from django.urls import path, re_path

from .consumers import ChatConsumer
from . import views


urlpatterns = [
    path('regole', views.Rules.as_view(), name='rules'),
    # TEMPORARY: CHAT
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]

socket_patterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]