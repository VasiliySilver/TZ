#!/bin/bash
set -e

# Используем POSTGRES_HOST из env переменной, по умолчанию localhost
POSTGRES_HOST=${POSTGRES_HOST:-localhost}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

echo "Waiting for database at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
  sleep 0.1
done
echo "Database is ready!"

echo "Running migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"