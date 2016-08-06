from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Preset
from tasks import ConfigHandler


def publish_preset(modeladmin, request, queryset):
    for preset in queryset:
        ch = ConfigHandler('/home/acserver/assetto-server/cfg')
        ch.write_server_config(preset)
        ch.write_entries_config(preset)


class PresetAdmin(admin.ModelAdmin):
    model = Preset
    filter_horizontal = ('cars', 'weathers')
    actions = [publish_preset]


admin.site.register(Preset, PresetAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
