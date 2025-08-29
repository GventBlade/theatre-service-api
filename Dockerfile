FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN useradd -m appuser
WORKDIR /code

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    netcat-openbsd \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY . .

RUN chmod +x /code/entrypoint.sh

RUN chown -R appuser:appuser /code
USER appuser

ENTRYPOINT ["sh", "/code/entrypoint.sh"]
CMD ["gunicorn", "theatre_service_api.wsgi:application", "--bind", "0.0.0.0:8000"]
