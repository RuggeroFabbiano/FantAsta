from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from auction.models import Club, Player


class Rules(LoginRequiredMixin, TemplateView):
    """Overview or auction rules before starting"""

    template_name = 'auction/rules.html'


class Room(LoginRequiredMixin, TemplateView):
    """Auction room"""

    template_name = 'auction/auction.html'

    def get_context_data(self, **kwargs):
        """Provide participant list"""
        context = super().get_context_data(**kwargs)
        context['clubs'] = Club.objects.all()
        return context


class PlayerList(View):
    """On AJAX requests, send list of players for current round"""

    def get(self, request, *args, **kwargs):
        """GET request"""
        players = Player.objects.filter(role=kwargs['role'], club__isnull=True)
        data = [
            {
                'id': p.id,
                'name': p.name,
                'team': p.team,
                'price': p.price
            } for p in players
        ]
        return JsonResponse(data, safe=False)


class ClubPlayerList(View):
    """On AJAX requests, send list of players of given club"""

    def get(self, request, *args, **kwargs):
        """GET request"""
        players = Player.objects.filter(club=request.user.club)
        data = [
            {
                'name': p.name,
                'role': p.role,
                'team': p.team,
                'price': p.price
            } for p in players
        ]
        return JsonResponse(data, safe=False)


# CHAT

def index(request):
    return render(request, "auction/index.html")

def room(request, room_name):
    return render(request, "auction/room.html", {"room_name": room_name})