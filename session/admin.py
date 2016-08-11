from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Preset, Entry
from .tasks import kick_services, ConfigHandler


def publish_preset(modeladmin, request, queryset):
    for preset in queryset:
        ch = ConfigHandler('/home/acserver/assetto-server/cfg')
        ch.write_server_config(preset)
        ch.write_entries_config(preset)
    kick_services()


class EntryInline(admin.StackedInline):
    model = Entry
    extra = 0


class EnvironmentAdmin(admin.ModelAdmin):
    model = Preset
    filter_horizontal = ('weathers',)
    inlines = [EntryInline]
    actions = [publish_preset]


admin.site.register(Preset, EnvironmentAdmin)
#admin.site.register(Entry)
#admin.site.unregister(User)
#admin.site.unregister(Group)
