# Dockerfile for Django + Gunicorn (for docker-compose)
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies (including MySQL client)
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install pipenv and copy dependency files
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies for MySQL
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy Django project
COPY . .

# Create static and media directories
RUN mkdir -p static media

# Collect static files (skip if no static files yet)
RUN python manage.py collectstatic --noinput --clear || true

# Expose port for Gunicorn
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "AiAgentWeb.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
