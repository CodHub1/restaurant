#!/bin/bash
set -e

python manage.py migrate --no-input
python manage.py loaddata data.json || true

exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
