from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms.fields import ChoiceField


class SignInForm(AuthenticationForm):
    """Sign-in form"""

    USERS = [
        (u.username, u.first_name) for u in User.objects.order_by('first_name')
    ]
    username = ChoiceField(
        label='', choices=[(None, 'Ti ricordi come ti chiami?')] + USERS
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['password'].label = "Di' la parolina magica:"