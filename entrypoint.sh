echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Postgres started"

python manage.py migrate --noinput

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser('admin@example.com', 'admin')" | python manage.py shell

if [ -f "./initial_data.json" ]; then
    python manage.py loaddata initial_data.json
    echo "Initial data loaded"
fi

exec "$@"
