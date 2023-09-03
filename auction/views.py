from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView, View

from auction.models import Club, Player


class Room(LoginRequiredMixin, TemplateView):
    """Auction room"""

    template_name = 'auction/auction.html'

    def get_context_data(self, **kwargs):
        """
        Provide participant list both as objects and as serialised data
        """
        context = super().get_context_data(**kwargs)
        clubs = Club.objects.all()
        context['participants'] = clubs
        context['clubs'] = list(clubs.values_list('name', flat=True))
        return context


class PlayerList(View):
    """On AJAX requests, send list of player for current round"""

    def get(self, request, *args, **kwargs):
        """GET request"""
        players = Player.objects.filter(role=kwargs['role'], club__isnull=True)
        data = [{'id': p.id, 'name': p.name, 'team': p.team, 'price': p.price} for p in players]
        return JsonResponse(data, safe=False)


class PlayerDetail(View):
    """On AJAX requests, send details of chosen player"""

    def get(self, request, *args, **kwargs):
        """GET request"""
        players = Player.objects.filter(role=kwargs['role'], club__isnull=True)
        data = [{'id': p.id, 'name': p.name, 'team': p.team, 'price': p.price} for p in players]
        return JsonResponse(data, safe=False)