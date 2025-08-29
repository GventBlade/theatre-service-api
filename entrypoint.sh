echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Postgres started"

python manage.py migrate --noinput
python manage.py loaddata initial_data.json

python manage.py collectstatic --noinput

exec gunicorn theatre_service_api.wsgi:application --bind 0.0.0.0:8000
