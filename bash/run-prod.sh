#!/usr/bin/env bash

python3 manage.py migrate && python3 manage.py collectstatic --noinput && gunicorn $WSGI_APP -b 0.0.0.0:8000 --log-file -