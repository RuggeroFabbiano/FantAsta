from django.contrib import admin
from django.urls import include, path, re_path

from .consumers import Consumer
from .views import Home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
]

socket_patterns = [re_path("asta", Consumer.as_asgi())]