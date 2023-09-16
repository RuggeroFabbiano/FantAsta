from django.contrib.admin import register
from django.contrib.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import Club, Player


@register(Club)
class ClubAdmin(ModelAdmin):
    """aaaa"""

    fields = ['name', 'money', 'user']


@register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    """aaa"""

    class PlayerResource(ModelResource):
        """aaa"""
        class Meta:
            model = Player

    resource_class = PlayerResource