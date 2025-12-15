#!/bin/sh
set -e

echo "Running database migrations..."

alembic upgrade head

echo "Starting Gunicorn"

exec gunicorn --workers ${WORKERS:-1} --bind 0.0.0.0:5000 "app:create_app()" 
