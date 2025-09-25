#!/usr/bin/env bash
set -e
set -x

echo "Aguardando Postgres em $DB_HOST:$DB_PORT..."


until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

echo "Postgres está pronto, rodando migrations..."

python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
