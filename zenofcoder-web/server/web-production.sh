#!/usr/bin/env bash

bash starting_point.sh

/usr/local/bin/gunicorn zenofcoder.wsgi:application \
--name zenofcoder_django \
--bind 0.0.0.0:8000 \
--workers 2 \
--log-level=info \
--error-logfile=/opt/zenofcoder/logs/gunicorn-error.log \
--log-file=/opt/zenofcoder/logs/gunicorn.log \
--access-logfile=/opt/zenofcoder/logs/gunicorn-access.log \
"$@"