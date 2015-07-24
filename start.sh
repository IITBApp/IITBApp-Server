fuser -k 9090/tcp
nohup gunicorn iitbapp.wsgi:application --timeout 600 --workers 10 --log-level=info --reload --bind=0.0.0.0:9090
