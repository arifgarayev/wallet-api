#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

echo "$PWD"

export PYTHONPATH="src/b2broker/"

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn \
    --bind 0.0.0.0:8000 config.wsgi \
    --capture-output \
    --worker-class gevent \
    --max-requests $GUNICORN_MAX_REQUESTS \
    --max-requests-jitter $GUNICORN_MAX_REQUESTS_JITTER \
    --workers $GUNICORN_WORKERS \
    --timeout $GUNICORN_TIMEOUT \
    --reload