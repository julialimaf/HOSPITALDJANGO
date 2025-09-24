#!/usr/bin/env bash
set -e
set -x

    python manage.py migrate --noinput
    python manage.py runserver 0.0.0.0:8000

