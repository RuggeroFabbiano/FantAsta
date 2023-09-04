# from random import choice
# from string import ascii_lowercase

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User
# from django.contrib.auth.views import LoginView
# from django.contrib.messages import success
# from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
# from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, TemplateView

# from .forms import SignInForm
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


# class SendPassowrd(RedirectView):
#     """
#     If user is still inactive, send him his password before redirecting
#     to log-in page
#     """

#     url = reverse_lazy('log-in')

#     def dispatch(self, request, *args, **kwargs):
#         user = User.objects.get(id=kwargs['id'])
#         if not user.is_active:
#             password = ''.join(choice(ascii_lowercase) for _ in range(8))
#             user.set_password(password)
#             user.is_active = True
#             user.save()
#             send_mail(
#                 "Le tue credenziali per la SuperFantaAsta",
#                 "Uhé testina!\n\n"
#                 "Qui sotto trovi le tue credenziali ⬇️\n"
#                 F"nome utente: {user}\n"
#                 F"parola magica: {password}\n\n"
#                 "Fa sö öna bèla squadra, dai!",
#                 from_email=None,
#                 recipient_list = [user.email],
#                 fail_silently = False
#             )
#             success(request, "Guarda la posta elettronica, bigol!")
#         return super().dispatch(request, *args, **kwargs)


# class SignIn(LoginView):
#     """Tweak Django log-in view"""

#     authentication_form = SignInForm
#     redirect_authenticated_user = True


# class Rules(LoginRequiredMixin, TemplateView):
#     """Overview or auction rules before starting"""

#     template_name = 'rules.html'