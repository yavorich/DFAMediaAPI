#!/bin/sh

until cd /app/rest
do
    echo "Waiting for server volume..."
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done


python manage.py collectstatic --noinput

python manage.py createsuperuser --noinput

python manage.py loaddata /app/rest/data.json

python manage.py runserver 0.0.0.0:8000