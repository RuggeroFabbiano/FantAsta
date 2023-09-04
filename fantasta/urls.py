from django.contrib import admin
from django.urls import include, path

# from admin import views as logs
# from auction import views as auction
# from .consumers import Consumer
from . import views


# urlpatterns = [
    # path("admin/logs", logs.Logs.as_view(), name="admin-logs"),
    # path("admin/logs/<str:log>", logs.Log.as_view(), name="admin-log"),
    # path('admin/', admin.site.urls),
    # path('', views.Home.as_view()),
    # path('connessione/<int:id>', views.SendPassowrd.as_view(), name="sign-in"),
    # path('connessione', views.SignIn.as_view(), name="log-in"),
    # path('regole', views.Rules.as_view(), name='rules'),
    # path('asta', auction.Room.as_view(), name='auction'),
    # path('players/<str:role>', auction.PlayerList.as_view(), name='players')
# ]

urlpatterns = [
    # path("admin/logs", logs.Logs.as_view(), name="admin-logs"),
    # path("admin/logs/<str:log>", logs.Log.as_view(), name="admin-log"),
    path("admin/", admin.site.urls),
    path("chat/", include("auction.urls")),  #! TEMP.
    path('', views.Home.as_view()),
    # path('connessione/<int:id>', views.SendPassowrd.as_view(), name="sign-in"),
    # path('connessione', views.SignIn.as_view(), name="log-in"),
    # path('regole', views.Rules.as_view(), name='rules'),
    # path('asta', auction.Room.as_view(), name='auction'),
    # path('players/<str:role>', auction.PlayerList.as_view(), name='players')
]