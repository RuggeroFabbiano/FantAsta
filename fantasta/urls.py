from django.contrib import admin
from django.urls import include, path

from .views import Home, Rules
from auction import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    path("conto/", include("account.urls")),
    path('regole', Rules.as_view(), name='rules'),
    path('asta', views.Room.as_view(), name='auction'),
    path('players/<str:role>', views.PlayerList.as_view(), name='players')
]