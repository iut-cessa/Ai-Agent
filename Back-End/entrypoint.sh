#!/bin/bash

echo "Waiting for database..."
while ! nc -z db 3306; do
  echo "Waiting for MySQL to be ready..."
  sleep 2
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
superuser_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
superuser_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
if not User.objects.filter(email=superuser_email).exists():
    User.objects.create_superuser(superuser_email, superuser_password)
    print(f'Superuser created with email: {superuser_email}')
else:
    print(f'Superuser already exists with email: {superuser_email}')
"

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 AiAgentWeb.wsgi:application
