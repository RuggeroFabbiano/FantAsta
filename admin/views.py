from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic import View

from auction.models import Club, Player


class Log(TemplateView):
    """Show log content"""

    template_name = 'admin/log.html'

    def get_context_data(self, **kwargs):
        """Pass log content to template"""
        context = super().get_context_data(**kwargs)
        with open(F"/logs/{kwargs['tool']}.log", 'r', encoding='UTF8') as log:
            context['content'] = log.read().strip('\n')
        return context


class Rosters(ListView):
    """Allow to choose a roster to visualise"""

    model = Club
    template_name = 'admin/rosters.html'


class Roster(DetailView):
    """Show given roster"""

    model = Club
    template_name = 'admin/roster.html'


class ClearRosters(View):
    """Clear rosters"""

    def get(self, request, *args, **kwargs):
        """Show confirmation button"""
        return render(request, 'admin/clear.html')

    def post(self, request, *args, **kwargs):
        """Clear rosters"""
        Player.objects.update(club=None)
        Club.objects.update(next_call=None)
        return redirect('home')