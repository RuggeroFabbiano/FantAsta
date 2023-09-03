from django.contrib.admin import register
from django.contrib.admin import ModelAdmin, site
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import Club, Player


site.register(Club, ModelAdmin)


@register(Player)
class PlayerAdmin(ImportExportModelAdmin):

    class PlayerResource(ModelResource):
        class Meta:
            model = Player

    resource_class = PlayerResource