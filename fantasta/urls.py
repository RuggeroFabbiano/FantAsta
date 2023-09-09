from django.contrib import admin
from django.urls import include, path

from admin.views import Log
# from auction import views as auction
# from .consumers import Consumer
# from . import views


urlpatterns = [
    path("admin/log", Log.as_view(), name="admin-log"),
    path("admin/", admin.site.urls),
    # path("asta/", include("auction.urls")),
    # path('', views.Home.as_view()),
    # path('connessione/<int:id>', views.SendPassowrd.as_view(), name="sign-in"),
    # path('connessione', views.SignIn.as_view(), name="log-in"),
]