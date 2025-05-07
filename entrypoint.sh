#!/bin/sh

set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.5
done
sleep 5
echo "PostgreSQL is ready."

# Run database migrations
python manage.py makemigrations
python manage.py migrate --noinput

# Start the Gunicorn server
gunicorn auth_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
