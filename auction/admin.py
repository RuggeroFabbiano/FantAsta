from django.contrib.admin import register
from django.contrib.admin import ModelAdmin, site
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import Club, Player


site.register(Club, ModelAdmin)

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
    fields = ['name', 'team', 'role', 'price']