from os import environ

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# import .urls
from .urls import socket_patterns


environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasta.settings')
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket':
            AllowedHostsOriginValidator(
                AuthMiddlewareStack(URLRouter(socket_patterns))
            )
    }
)


