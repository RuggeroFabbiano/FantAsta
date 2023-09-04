from os import environ

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create super user"""

    def handle(self, *args, **kwargs):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                'Gero', 'ruggero.fabbiano@gmail.com', environ['ADMIN_PASSWORD']
            )