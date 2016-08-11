from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Environment, EntryGroup, Entry
from .tasks import kick_services, ConfigHandler


def publish_preset(modeladmin, request, queryset):
    for preset in queryset:
        ch = ConfigHandler('/home/acserver/assetto-server/cfg')
        ch.write_server_config(preset)
        ch.write_entries_config(preset)

    kick_services()


class EntryGroupInline(admin.StackedInline):
    model = EntryGroup
    extra = 1

class EnvironmentAdmin(admin.ModelAdmin):
    model = Environment
    filter_horizontal = ('weathers',)
    inlines = [EntryGroupInline]


class EntryInline(admin.StackedInline):
    model = Entry
    extra = 0


class EntryGroupAdmin(admin.ModelAdmin):
    model = EntryGroup
    #filter_horizontal = ('cars',)
    actions = [publish_preset]
    inlines = [EntryInline]


admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(EntryGroup, EntryGroupAdmin)
admin.site.register(Entry)
admin.site.unregister(User)
admin.site.unregister(Group)
