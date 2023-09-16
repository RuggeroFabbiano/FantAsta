from django.urls import path, re_path

from .consumers import Consumer
from . import views


urlpatterns = [
    path("regole", views.Rules.as_view(), name="rules"),
    path("", views.Room.as_view(), name="auction"),
    path("players/<str:role>", views.PlayerList.as_view(), name="players"),
    path("players", views.ClubPlayerList.as_view(), name="players-club"),
]

socket_patterns = [re_path("ws/asta/", Consumer.as_asgi())]