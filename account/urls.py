from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('connessione/<int:id>', views.SendPassowrd.as_view(), name="sign-in"),
    path('connessione', views.SignIn.as_view(), name="log-in")
]
