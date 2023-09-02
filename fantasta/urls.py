from django.contrib import admin
from django.urls import include, path

from .views import Home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
]