from os import environ

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasta.settings')
asgi_app = get_asgi_application()

from auction.urls import socket_patterns

application = ProtocolTypeRouter(
    {
        'http': asgi_app,
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(socket_patterns))
        )
    }
)