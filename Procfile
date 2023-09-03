web: nginx --bind :8000 --workers 3 --threads 2 fantasta.wsgi:application
websocket: daphne -b :: -p 5000 fantasta.asgi:application