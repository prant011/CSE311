#!/bin/bash

# Run migrations if database is empty
python manage.py migrate --run-syncdb

# Collect static files
python manage.py collectstatic --noinput

# Start the server
exec gunicorn library_project.wsgi:application --bind 0.0.0.0:$PORT
