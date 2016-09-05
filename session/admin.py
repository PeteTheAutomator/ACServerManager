from django.contrib import admin
from .models import ServerSetting, Preset, Entry
from .tasks import get_server_status


class ServerSettingsAdmin(admin.ModelAdmin):
    model = ServerSetting
    actions = None

    fieldsets = (
        (None, {
            'fields': ('name', 'welcome_message', 'admin_password', 'minorating_grade'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('udp_port', 'tcp_port', 'http_port', 'send_buffer_size', 'recv_buffer_size',
                       'client_send_interval', 'minorating_server_trust_token', 'proxy_plugin_port',
                       'proxy_plugin_local_port'),
        })
    )


class EntryInline(admin.StackedInline):
    model = Entry
    extra = 0

    fieldsets = (
        (None, {
            'fields': ('car', 'skin',),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('name', 'fixed_setup', 'spectator_mode', 'team', 'guid', 'ballast'),
        })
    )


class PresetAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        # This try block is to overcome initial schema migrations where the background_task model isn't present
        try:
            get_server_status()
        except:
            pass
        super(PresetAdmin, self).__init__(*args, **kwargs)


    fieldsets = (
        (None, {
            'fields': ('name', 'server_setting',),
        }),
        ('Environmental conditions', {
            'fields': ('track', 'track_dynamism', 'weathers', 'time_of_day'),
        }),
        ('Session type', {
            'fields': ('practice_time', 'practice_is_open', 'qualify_time', 'qualify_is_open', 'race_laps',
                       'race_wait_time', 'race_is_open'),
        }),
        ('Car management', {
            'fields': (
            'tc_allowed', 'abs_allowed', 'stability_allowed', 'autoclutch_allowed', 'force_virtual_mirror',
            'damage_multiplier', 'fuel_rate', 'tyre_blankets_allowed', 'tyre_wear_rate', 'allowed_tyres_out'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('max_clients', 'pickup_mode_enabled', 'session_password', 'voting_quorum', 'vote_duration',
                       'kick_quorum', 'race_over_time', 'loop_mode', 'blacklist_mode', 'qualify_max_wait_perc',
                       'start_rule')
        }),
    )

    model = Preset
    filter_horizontal = ('weathers',)
    inlines = [EntryInline]
    save_as = True
    list_display = ('__unicode__', 'launch_configuration', 'stop_configuration', 'acserver_status', 'stracker_status',
                    'minorating_status')
    exclude = ('acserver_run_status', 'stracker_run_status', 'minorating_run_status')
    #actions = None

    def launch_configuration(self, obj):
        if not obj.acserver_run_status and not obj.stracker_run_status and not obj.minorating_run_status:
            return '<a href="/admin/session/preset/' + str(obj.pk) + '/launch/">Launch</a>'
        else:
            return '<a href="/admin/session/preset/' + str(obj.pk) + '/launch/">Re-launch</a>'
    launch_configuration.allow_tags = True

    def stop_configuration(self, obj):
        if not obj.acserver_run_status and not obj.stracker_run_status and not obj.minorating_run_status:
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

    def minorating_status(self, obj):
        if obj.minorating_run_status:
            return 'running'
        else:
            return 'stopped'


admin.site.register(ServerSetting, ServerSettingsAdmin)
admin.site.register(Preset, PresetAdmin)
