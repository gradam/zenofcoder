#!/usr/bin/env bash

bash starting_point.sh

# create admin user if doesn't exist
echo "from django.contrib.auth.models import User;User.objects.create_superuser('admin', 'kuba.semik@gmail.com', 'admin') if not User.objects.filter(username='admin').exists() else print('admin already created')" | python manage.py shell


/usr/local/bin/gunicorn zenofcoder.wsgi:application \
--name zenofcoder_django \
--bind 0.0.0.0:8000 \
--workers 2 \
--log-level=debug \
--reload \
--error-logfile=/opt/zenofcoder/logs/gunicorn-error.log \
--log-file=/opt/zenofcoder/logs/gunicorn.log \
--access-logfile=/opt/zenofcoder/logs/gunicorn-access.log \
"$@"