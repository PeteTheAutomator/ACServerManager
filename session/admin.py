from django.contrib import admin
from .models import ServerSetting, Preset, Entry
from .tasks import kick_services, write_config, get_server_status


def publish_preset(modeladmin, request, queryset):
    for preset in queryset:
        write_config(preset_id=preset.id)
        kick_services(preset_id=preset.id)
        get_server_status()


class EntryInline(admin.StackedInline):
    model = Entry
    extra = 0


class PresetAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        # This try block is to overcome initial schema migrations where the background_task model isn't present
        try:
            get_server_status()
        except:
            pass
        super(PresetAdmin, self).__init__(*args, **kwargs)

    model = Preset
    filter_horizontal = ('weathers',)
    inlines = [EntryInline]
    save_as = True
    list_display = ('__unicode__', 'launch_configuration', 'acserver_status', 'stracker_status')
    exclude = ('acserver_run_status', 'stracker_run_status',)

    def launch_configuration(self, obj):
        return '<a href="/session/preset/' + str(obj.pk) + '/launch/">Launch This Server Configuration</a>'
    launch_configuration.allow_tags = True

    def acserver_status(self, obj):
        if obj.acserver_run_status:
            return 'running'
        else:
            return 'stopped'

    def stracker_status(self, obj):
        if obj.stracker_run_status:
            return 'running'
        else:
            return 'stopped'


admin.site.register(ServerSetting)
admin.site.register(Preset, PresetAdmin)
