#!/usr/bin/env bash

python3 manage.py migrate
chown -R "$USER:$USER" static/
python3 manage.py collectstatic --no-input --clear --verbosity 0
exec gunicorn --bind 0.0.0.0:8000 noxcrux.wsgi
