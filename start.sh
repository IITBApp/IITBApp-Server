#!/bin/bash
PORT=9090

while getopts p: opt; do
  case $opt in
  p)
      PORT=$OPTARG
      ;;
  esac
done

fuser -k $PORT/tcp
gunicorn iitbapp.wsgi \
    --bind=0.0.0.0:$PORT \
     -c gunicorn_conf.py \
    --log-level=info \
    --reload \
    --log-file "logs/gunicorn_logs.log" &
