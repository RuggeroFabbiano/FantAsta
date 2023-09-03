#!/bin/bash
source /fantastenv/bin/activate
cd /code

echo "----- Collect static files -----"
python manage.py collectstatic --noinput

echo "----- Apply migrations -----"
python manage.py makemigrations
python manage.py migrate

echo "----- Run Django local server -----"
python manage.py runserver 0.0.0.0:8000