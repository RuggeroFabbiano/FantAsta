from django.contrib.admin import register
from django.contrib.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import Club, Player


@register(Club)
class ClubAdmin(ModelAdmin):
    """Club participating to the ligue"""

    fields = ['name', 'user']


@register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    """Serie A player"""

    class PlayerResource(ModelResource):
        """Import/export resource"""
        class Meta:
            model = Player

    resource_class = PlayerResource