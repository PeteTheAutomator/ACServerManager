from django.contrib import admin
from .models import ServerSetting, Preset, Entry
from .tasks import kick_services, write_config


def publish_preset(modeladmin, request, queryset):
    for preset in queryset:
        write_config(preset_id=preset.id)
    kick_services()


class EntryInline(admin.StackedInline):
    model = Entry
    extra = 0


class EnvironmentAdmin(admin.ModelAdmin):
    model = Preset
    filter_horizontal = ('weathers',)
    inlines = [EntryInline]
    actions = [publish_preset]
    save_as = True
    list_display = ('__unicode__', 'launch_configuration')

    # TODO: hook this up to a new view which provides some feedback into the publish_preset method
    # above, and ideally some output from the background task which kicks services
    def launch_configuration(self, obj):
        return '<a href="' + str(obj.pk) + '">Launch This Server Configuration</a>'
    launch_configuration.allow_tags = True


admin.site.register(ServerSetting)
admin.site.register(Preset, EnvironmentAdmin)
