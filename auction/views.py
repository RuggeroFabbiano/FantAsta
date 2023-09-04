from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class Rules(LoginRequiredMixin, TemplateView):
    """Overview or auction rules before starting"""

    template_name = 'auction/rules.html'











def index(request):
    return render(request, "auction/index.html")



def room(request, room_name):
    return render(request, "auction/room.html", {"room_name": room_name})