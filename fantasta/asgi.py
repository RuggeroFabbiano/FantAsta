from os import environ

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# import .urls
# from .urls import socket_patterns


environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasta.settings')
# import auction.routing
application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket':
            AllowedHostsOriginValidator(
                AuthMiddlewareStack(URLRouter(auction.routing.websocket_urlpatterns))  # socket_patterns
            )
    }
)