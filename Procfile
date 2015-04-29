web: gunicorn localshop.wsgi --log-file -
worker: localshop celery worker -B -E -c 1
