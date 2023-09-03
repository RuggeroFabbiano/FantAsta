# from os import environ

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.core.asgi import get_asgi_application

# # import .urls
# from .urls import socket_patterns


# environ.setdefault('DJANGO_SETTINGS_MODULE', 'fantasta.settings')
# application = ProtocolTypeRouter(
#     {
#         'http': get_asgi_application(),
#         'websocket':
#             AllowedHostsOriginValidator(
#                 AuthMiddlewareStack(URLRouter(socket_patterns))
#             )
#     }
# )


import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import auction.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(auction.routing.websocket_urlpatterns))
        ),
    }
)