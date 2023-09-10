from os import environ

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django import setup
from django.core.asgi import get_asgi_application
import django

from auction.urls import socket_patterns


environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasta.settings')
django.setup()
application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket':
            AllowedHostsOriginValidator(
                AuthMiddlewareStack(URLRouter(socket_patterns))
            )
    }
)