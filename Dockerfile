FROM python:3.13.6-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser
USER appuser

command: ["sh", "/code/entrypoint.sh", "gunicorn", "theatre_service_api.wsgi:application", "--bind", "0.0.0.0:8000"]

