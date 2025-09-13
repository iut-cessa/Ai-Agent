#!/bin/bash

# Create logs directory if it doesn't exist
echo "Creating logs directory..."
mkdir -p /app/logs
chmod 755 /app/logs

echo "Waiting for database..."
while ! nc -z db 3306; do
  echo "Waiting for MySQL to be ready..."
  sleep 2
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser if not exists..."
python manage.py create_superuser_safe

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 AiAgentWeb.wsgi:application
