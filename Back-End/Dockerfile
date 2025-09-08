# Use Python 3.11 (more stable for Django)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=AiAgentWeb.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
        curl \
        netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create static and media directories
RUN mkdir -p /app/static /app/media

# Skip collectstatic during build (run it at runtime instead)
# This avoids database connection issues during build

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Create an entrypoint script to run migrations and collectstatic at startup
USER root
RUN echo '#!/bin/bash\n\
echo "Waiting for database..."\n\
while ! nc -z db 3306; do\n\
  echo "Waiting for MySQL to be ready..."\n\
  sleep 2\n\
done\n\
echo "Database is ready!"\n\
\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput\n\
\n\
echo "Creating superuser if not exists..."\n\
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email=\"admin@admin.com\").exists() or User.objects.create_superuser(\"admin@admin.com\", \"admin123\")"\n\
\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput --clear\n\
\n\
echo "Starting Gunicorn..."\n\
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 AiAgentWeb.wsgi:application' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh
RUN chown appuser:appuser /app/entrypoint.sh

USER appuser

# Use the entrypoint script
CMD ["/app/entrypoint.sh"]
