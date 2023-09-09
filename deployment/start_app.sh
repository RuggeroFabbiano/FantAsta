#!/bin/bash
source /fantastenv/bin/activate
cd /code

echo "\n----- Collect static files -----" 
python manage.py collectstatic --noinput

echo "\n----- Apply migrations -----"
python manage.py migrate auth
python manage.py makemigrations 
python manage.py migrate

echo "\n----- Run GUnicorn -----"
gunicorn -b :8000 fantasta.wsgi:application