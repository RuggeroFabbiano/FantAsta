#!/bin/bash
source /fantastenv/bin/activate
cd /code

echo "" 
echo "----- Collect static files -----" 
python manage.py collectstatic --noinput

echo "" 
echo "----- Apply migrations -----"
python manage.py migrate auth
python manage.py makemigrations 
python manage.py migrate

echo "" 
echo "----- Create superuser -----"
python manage.py create_administrator

echo "" 
echo "----- Run GUnicorn -----"
gunicorn -b :8000 fantasta.wsgi:application