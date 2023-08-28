from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from auction.models import Club


class Home(ListView):
    """Home page"""

    template_name = 'home.html'
    model = Club

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Check if user is already authenticated before rendering the page"""
        if request.user.is_authenticated:
            return redirect('rules')
        return super().dispatch(request, *args, **kwargs)


class Rules(LoginRequiredMixin, TemplateView):
    """Overview or auction rules before starting"""

    template_name = 'rules.html'