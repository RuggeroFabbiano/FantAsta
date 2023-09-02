from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView, View


class Home(View):
    """Home page"""

    def get(self, request, *args, **kwargs):
        return HttpResponse("OK")