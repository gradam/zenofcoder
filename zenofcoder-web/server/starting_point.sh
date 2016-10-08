#!/usr/bin/env bash
# wait for postgres being ready to respond
python wait_for_postgres.py
python manage.py migrate
python manage.py collectstatic --no-input

# Prepare log files and start outputting logs to stdout
mkdir -p /opt/zenofcoder/logs
touch /opt/zenofcoder/logs/gunicorn.log
touch /opt/zenofcoder/logs/gunicorn-access.log
touch /opt/zenofcoder/logs/gunicorn-error.log
touch /opt/zenofcoder/logs/nginx-access.log
touch /opt/zenofcoder/logs/nginx-error.log
touch /opt/zenofcoder/logs/django-errors.log
touch /opt/zenofcoder/logs/django-debug.log
tail -n 0 -f /opt/zenofcoder/logs/*.log &

