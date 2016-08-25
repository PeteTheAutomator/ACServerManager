from django.contrib import admin
from .models import ServerSetting, Preset, Entry
from .tasks import get_server_status


class ServerSettingsAdmin(admin.ModelAdmin):
    model = ServerSetting
    actions = None


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
    list_display = ('__unicode__', 'launch_configuration', 'stop_configuration', 'acserver_status', 'stracker_status')
    exclude = ('acserver_run_status', 'stracker_run_status',)
    actions = None

    # stop / start / relaunch
    # - if both acserver and stracker are down - launch
    # - if both acserver and stracker are running - stop/restart
    # - if in a mixed state - stop/restart
    def launch_configuration(self, obj):
        if not obj.acserver_run_status and not obj.stracker_run_status:
            return '<a href="/admin/session/preset/' + str(obj.pk) + '/launch/">Launch</a>'
        else:
            return '<a href="/admin/session/preset/' + str(obj.pk) + '/launch/">Re-launch</a>'
    launch_configuration.allow_tags = True

    def stop_configuration(self, obj):
        if not obj.acserver_run_status and not obj.stracker_run_status:
            return ' - '
        else:
            return '<a href="/admin/session/preset/' + str(obj.pk) + '/stop/">Stop</a>'
    stop_configuration.allow_tags = True

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


admin.site.register(ServerSetting, ServerSettingsAdmin)
admin.site.register(Preset, PresetAdmin)
