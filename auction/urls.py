from django.urls import path, re_path

from .consumers import Consumer, ChatConsumer  # CHAT
from . import views


urlpatterns = [
    path("regole", views.Rules.as_view(), name="rules"),
    path("", views.Room.as_view(), name="auction"),
    path("players/<str:role>", views.PlayerList.as_view(), name="players"),
    path("players", views.ClubPlayerList.as_view(), name="players-club"),
    # CHAT
    path("room", views.index, name="index"),
    path("room/<str:room_name>/", views.room, name="room")
]

socket_patterns = [
    re_path(r"ws/asta/room/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),  # CHAT
    re_path("ws/asta/", Consumer.as_asgi())
]