from django.contrib import admin
from django.urls import include, path, re_path

# from admin.views import Log
# from auction import views
from .consumers import Consumer
from . import views


urlpatterns = [
    # path("admin/log", Log.as_view(), name="admin-log"),
    path('admin/', admin.site.urls),
    path('', views.Home.as_view()),
    # path("conto/", include("account.urls")),
    # path('regole', views.Rules.as_view(), name='rules'),
    # path('asta', viewsAuction.Room.as_view(), name='auction'),
    # path('players/<str:role>', viewsAuction.PlayerList.as_view(), name='players')
]

socket_patterns = [re_path("asta", Consumer.as_asgi())]