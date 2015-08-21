#!/bin/bash
fuser -k 9090/tcp
nohup gunicorn iitbapp.wsgi:application \
    --timeout 600 \
    --workers 10 \
    --log-level=info \
    --reload \
    --bind=0.0.0.0:9090 \
    --access-logformat "%(h)s %(D)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s" \
    --access-logfile "logs/gunicorn_access.log" \
    --error-logfile "logs/gunicorn_error.log" \
    --log-file "logs/gunicorn_logs.log" &
