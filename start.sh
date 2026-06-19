#!/usr/bin/env bash
set -e

python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py loaddata data.json || true
python manage.py sync_image_paths || true

exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
