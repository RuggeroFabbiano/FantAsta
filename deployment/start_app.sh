#!/bin/bash
source /fantastenv/bin/activate
cd /code

echo "----- Collect static files -----" 
python manage.py collectstatic --noinput

echo "----- Apply migrations -----"
python manage.py makemigrations 
python manage.py migrate

echo "----- Run GUnicorn -----"
gunicorn -b :8000 fantasta.wsgi:application