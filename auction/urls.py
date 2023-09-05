from django.urls import path, re_path

from .consumers import ChatConsumer
from . import views


urlpatterns = [
    path('regole', views.Rules.as_view(), name='rules'),
    # path('asta', auction.Room.as_view(), name='auction'),
    # path('players/<str:role>', auction.PlayerList.as_view(), name='players')
    # TEMPORARY: CHAT
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]

socket_patterns = [
    re_path(r"ws/asta/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]