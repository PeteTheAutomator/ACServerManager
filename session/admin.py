from django.contrib import admin
from .models import ServerSetting, Preset, Entry
from .tasks import kick_services, write_config, get_server_status


def publish_preset(modeladmin, request, queryset):
    for preset in queryset:
        write_config(preset_id=preset.id)
        kick_services(preset_id=preset.id)


class EntryInline(admin.StackedInline):
    model = Entry
    extra = 0


class PresetAdmin(admin.ModelAdmin):
    '''
    def __init__(self, *args, **kwargs):
        get_server_status()
        super(PresetAdmin, self).__init__(*args, **kwargs)
    '''

    model = Preset
    filter_horizontal = ('weathers',)
    inlines = [EntryInline]
    actions = [publish_preset]
    save_as = True
    list_display = ('__unicode__', 'launch_configuration')
    exclude = ('acserver_run_status', 'stracker_run_status',)

    # TODO: hook this up to a new view which provides some feedback into the publish_preset method
    # above, and ideally some output from the background task which kicks services
    def launch_configuration(self, obj):
        return '<a href="/session/preset/' + str(obj.pk) + '/launch/">Launch This Server Configuration</a>'
    launch_configuration.allow_tags = True


admin.site.register(ServerSetting)
admin.site.register(Preset, PresetAdmin)
