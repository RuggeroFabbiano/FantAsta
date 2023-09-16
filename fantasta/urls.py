from django.contrib import admin
from django.urls import include, path

from admin.views import ClearRosters, Log, Roster, Rosters
from . import views


urlpatterns = [
    path("admin/rosters", Rosters.as_view(), name="admin-rosters"),
    path("admin/rosters/<int:pk>", Roster.as_view(), name="admin-roster"),
    path("admin/clear", ClearRosters.as_view(), name="admin-clear"),
    path("admin/log/<str:tool>", Log.as_view(), name="admin-log"),
    path("admin/", admin.site.urls),
    path('', views.Home.as_view(), name="home"),
    path("connessione/<int:id>", views.SendPassowrd.as_view(), name="sign-in"),
    path("connessione", views.SignIn.as_view(), name="log-in"),
    path("asta/", include('auction.urls'))
]