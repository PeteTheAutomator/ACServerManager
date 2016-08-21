import os
from configparser import ConfigParser
from background_task import background
from datetime import datetime, timedelta
from .models import Preset
from django.conf import settings
from subprocess import Popen, PIPE
import re


@background(schedule=timedelta(seconds=0))
def write_config(preset_id):
    preset = Preset.objects.get(id=preset_id)
    acserver_config_dir = os.path.join(settings.ACSERVER_CONFIG_DIR, str(preset_id))
    stracker_config_dir = os.path.join(settings.STRACKER_CONFIG_DIR, str(preset_id))
    ch = ConfigHandler(acserver_config_dir, stracker_config_dir)
    ch.write_acserver_config(preset)
    ch.write_entries_config(preset)
    ch.write_welcome_message(preset)
    ch.write_stracker_config(preset)


@background(schedule=timedelta(seconds=1))
def kick_services(preset_id):
    p = Popen(['/bin/sudo', '/usr/bin/systemctl', 'restart', 'acserver@' + str(preset_id)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.communicate()
    acserver_return_code = p.returncode

    if acserver_return_code != 0:
        raise Exception('failed to restart assetto corsa server process')

    p = Popen(['/bin/sudo', '/usr/bin/systemctl', 'restart', 'stracker@' + str(preset_id)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.communicate()
    stracker_return_code = p.returncode
    if stracker_return_code != 0:
        raise Exception('failed to restart stracker server process')


@background(schedule=timedelta(seconds=0))
def get_server_status():
    p = Popen(['/bin/sudo', '/usr/bin/systemctl', 'list-units'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    if rc == 0:
        output_lines = output.split('\n')
        for preset in Preset.objects.all():
            preset_changed = False
            acserver_regex = re.compile('\s*acserver@' + str(preset.id) + '\.service\s+loaded active running')
            stracker_regex = re.compile('\s*stracker@' + str(preset.id) + '\.service\s+loaded active running')
            for line in output_lines:
                if re.match(acserver_regex, line):
                    if not preset.acserver_run_status:
                        preset.acserver_run_status = True
                        preset_changed = True
                if re.match(stracker_regex, line):
                    if not preset.stracker_run_status:
                        preset.stracker_run_status = True
                        preset_changed = True
            if preset_changed:
                preset.save()
        

def time_to_sun_angle(time):
    return str((time.hour - 13) * 16)


class ConfigHandler:
    def __init__(self, acserver_config_dir, stracker_config_dir):
        self.acserver_config_dir = acserver_config_dir
        self.stracker_config_dir = stracker_config_dir

        if not os.path.isdir(self.acserver_config_dir):
            os.makedirs(self.acserver_config_dir)

        if not os.path.isdir(self.stracker_config_dir):
            os.makedirs(self.stracker_config_dir)

    def write_acserver_config(self, preset):
        config = ConfigParser()
        config.optionxform = str
        cfg_file = open(os.path.join(self.acserver_config_dir, 'server_cfg.ini'), 'w')
        config.add_section('SERVER')

        # build a distinct list of car names
        car_list = []
        for driver in preset.entry_set.all():
            if driver.car.dirname not in car_list:
                car_list.append(driver.car.dirname)

        # set max_clients value to the track's pitbox value if null
        if not preset.max_clients:
            preset.max_clients = preset.track.pitboxes

        config.set('SERVER', 'NAME', preset.server_setting.name)
        config.set('SERVER', 'CARS', ','.join(car_list))
        config.set('SERVER', 'CONFIG_TRACK', '' if not preset.track.subversion else preset.track.subversion)
        config.set('SERVER', 'TRACK', preset.track.dirname)
        config.set('SERVER', 'SUN_ANGLE', time_to_sun_angle(preset.time_of_day))
        config.set('SERVER', 'PASSWORD', str(preset.session_password))
        config.set('SERVER', 'ADMIN_PASSWORD', str(preset.server_setting.admin_password))
        config.set('SERVER', 'UDP_PORT', str(preset.server_setting.udp_port))
        config.set('SERVER', 'TCP_PORT', str(preset.server_setting.tcp_port))
        config.set('SERVER', 'HTTP_PORT', str(preset.server_setting.http_port))
        config.set('SERVER', 'PICKUP_MODE_ENABLED', str(int(preset.pickup_mode_enabled)))
        config.set('SERVER', 'LOOP_MODE', str(int(preset.loop_mode)))
        config.set('SERVER', 'SLEEP_TIME', '1')
        config.set('SERVER', 'CLIENT_SEND_INTERVAL', str(preset.server_setting.client_send_interval))
        config.set('SERVER', 'SEND_BUFFER_SIZE', str(preset.server_setting.send_buffer_size))
        config.set('SERVER', 'RECV_BUFFER_SIZE', str(preset.server_setting.recv_buffer_size))
        config.set('SERVER', 'RACE_OVER_TIME', str(preset.race_over_time))
        config.set('SERVER', 'KICK_QUORUM', str(preset.kick_quorum))
        config.set('SERVER', 'VOTING_QUORUM', str(preset.voting_quorum))
        config.set('SERVER', 'VOTE_DURATION', str(preset.vote_duration))
        config.set('SERVER', 'BLACKLIST_MODE', str(preset.blacklist_mode))
        config.set('SERVER', 'FUEL_RATE', str(preset.fuel_rate))
        config.set('SERVER', 'DAMAGE_MULTIPLIER', str(preset.damage_multiplier))
        config.set('SERVER', 'TYRE_WEAR_RATE', str(preset.tyre_wear_rate))
        config.set('SERVER', 'ALLOWED_TYRES_OUT', str(preset.allowed_tyres_out))
        config.set('SERVER', 'ABS_ALLOWED', str(preset.abs_allowed))
        config.set('SERVER', 'TC_ALLOWED', str(preset.tc_allowed))
        config.set('SERVER', 'STABILITY_ALLOWED', str(int(preset.stability_allowed)))
        config.set('SERVER', 'AUTOCLUTCH_ALLOWED', str(int(preset.autoclutch_allowed)))
        config.set('SERVER', 'TYRE_BLANKETS_ALLOWED', str(int(preset.tyre_blankets_allowed)))
        config.set('SERVER', 'FORCE_VIRTUAL_MIRROR', str(int(preset.force_virtual_mirror)))
        config.set('SERVER', 'REGISTER_TO_LOBBY', '1')
        config.set('SERVER', 'MAX_CLIENTS', str(preset.max_clients))
        config.set('SERVER', 'UDP_PLUGIN_LOCAL_PORT', '11000')
        config.set('SERVER', 'UDP_PLUGIN_ADDRESS', '127.0.0.1:12000')
        config.set('SERVER', 'AUTH_PLUGIN_ADDRESS', '')
        config.set('SERVER', 'LEGAL_TYRES', 'V;E;HR;ST')

        if preset.server_setting.welcome_message:
            config.set('SERVER', 'WELCOME_MESSAGE', str(os.path.join(self.acserver_config_dir, 'welcome_message.txt')))

        if preset.practice:
            config.add_section('PRACTICE')
            config.set('PRACTICE', 'NAME', 'Free Practice')
            config.set('PRACTICE', 'TIME', str(preset.practice_time))
            config.set('PRACTICE', 'IS_OPEN', str(int(preset.practice_is_open)))

        if preset.qualify:
            config.add_section('QUALIFY')
            config.set('QUALIFY', 'NAME', 'Qualify')
            config.set('QUALIFY', 'TIME', str(preset.qualify_time))
            config.set('QUALIFY', 'IS_OPEN', str(int(preset.qualify_is_open)))

        if preset.race:
            config.add_section('RACE')
            config.set('RACE', 'NAME', 'Race')
            config.set('RACE', 'LAPS', str(preset.race_laps))
            config.set('RACE', 'WAIT_TIME', str(preset.race_wait_time))
            config.set('RACE', 'IS_OPEN', str(preset.race_is_open))

        if preset.track_dynamism:
            config.add_section('DYNAMIC_TRACK')
            config.set('DYNAMIC_TRACK', 'SESSION_START', str(preset.track_dynamism.session_start))
            config.set('DYNAMIC_TRACK', 'RANDOMNESS', str(preset.track_dynamism.randomness))
            config.set('DYNAMIC_TRACK', 'SESSION_TRANSFER', str(preset.track_dynamism.session_transfer))
            config.set('DYNAMIC_TRACK', 'LAP_GAIN', str(preset.track_dynamism.lap_gain))

        weather_count = 0
        for weather in preset.weathers.all():
            weather_section = 'WEATHER_' + str(weather_count)
            config.add_section(weather_section)
            config.set(weather_section, 'GRAPHICS', weather.graphics)
            config.set(weather_section, 'BASE_TEMPERATURE_AMBIENT', str(weather.base_temperature_ambient))
            config.set(weather_section, 'VARIATION_AMBIENT', str(weather.variation_ambient))
            config.set(weather_section, 'BASE_TEMPERATURE_ROAD', str(weather.base_temperature_road))
            config.set(weather_section, 'VARIATION_ROAD', str(weather.variation_road))
            weather_count += 1

        config.write(cfg_file, space_around_delimiters=False)
        cfg_file.close()

    def write_entries_config(self, preset):
        config = ConfigParser()
        config.optionxform = str
        cfg_file = open(os.path.join(self.acserver_config_dir, 'entry_list.ini'), 'w')
        car_count = 0

        for entry in preset.entry_set.all():
            car_section = 'CAR_' + str(car_count)
            config.add_section(car_section)
            config.set(car_section, 'MODEL', entry.car.dirname)
            config.set(car_section, 'SKIN', entry.skin.name)
            config.set(car_section, 'SPECTATOR_MODE', str(int(entry.spectator_mode)))
            config.set(car_section, 'DRIVER_NAME', entry.name)
            config.set(car_section, 'TEAM', entry.team)
            config.set(car_section, 'GUID', entry.guid)
            config.set(car_section, 'BALLAST', str(entry.ballast))
            car_count += 1

        config.write(cfg_file, space_around_delimiters=False)
        cfg_file.close()

    def write_welcome_message(self, preset):
        fh = open(os.path.join(self.acserver_config_dir, 'welcome_message.txt'), 'w')
        fh.write(preset.server_setting.welcome_message)
        fh.close()

    def write_stracker_config(self, preset):
        # If we're going to allow multiple instances of acserver, then we need to allow multiple instances of stracker
        # or at least have the ability to configure which acserver instance config to use.  Most of these parameters are
        # static for now - over time they can be added to the ServerSettings model.
        config = ConfigParser()
        config.optionxform = str
        cfg_file = open(os.path.join(self.stracker_config_dir, 'stracker.ini'), 'w')
        config.add_section('STRACKER_CONFIG')
        config.set('STRACKER_CONFIG', 'ac_server_address', '127.0.0.1')
        config.set('STRACKER_CONFIG', 'ac_server_cfg_ini', os.path.join(self.acserver_config_dir, 'server_cfg.ini'))
        config.set('STRACKER_CONFIG', 'append_log_file', 'False')
        config.set('STRACKER_CONFIG', 'keep_alive_ptracker_conns', 'True')
        config.set('STRACKER_CONFIG', 'listening_port', '50042')
        # TODO: put the log_file somewhere sensible
        config.set('STRACKER_CONFIG', 'log_file', os.path.join(self.stracker_config_dir, 'stracker.log'))
        config.set('STRACKER_CONFIG', 'log_level', 'info')
        config.set('STRACKER_CONFIG', 'log_timestamps', 'False')
        config.set('STRACKER_CONFIG', 'lower_priority', 'True')
        config.set('STRACKER_CONFIG', 'perform_checksum_comparisons', 'False')
        config.set('STRACKER_CONFIG', 'ptracker_connection_mode', 'any')
        config.set('STRACKER_CONFIG', 'server_name', 'acserver')
        config.set('STRACKER_CONFIG', 'tee_to_stdout', 'False')

        config.add_section('SWEAR_FILTER')
        config.set('SWEAR_FILTER', 'action', 'none')
        config.set('SWEAR_FILTER', 'ban_duration', '30')
        config.set('SWEAR_FILTER', 'num_warnings', '3')
        config.set('SWEAR_FILTER', 'swear_file', 'bad_words.txt')
        # TODO: the warning message below originally took parameterised "action" and "num_warnings" values; this caused ConfigParser issues so the message was made static.  Ideally this wants to become dynamic somehow.
        config.set('SWEAR_FILTER', 'warning',
                   'Please be polite and do not swear in the chat. You will be kicked from the server after receiving 3 more warnings.')

        config.add_section('SESSION_MANAGEMENT')
        config.set('SESSION_MANAGEMENT', 'race_over_strategy', 'none')
        config.set('SESSION_MANAGEMENT', 'wait_secs_before_skip', '15')

        config.add_section('MESSAGES')
        config.set('MESSAGES', 'best_lap_time_broadcast_threshold', '105')
        config.set('MESSAGES', 'car_to_car_collision_msg', 'True')
        config.set('MESSAGES', 'message_types_to_send_over_chat', 'best_lap+welcome+race_finished')

        config.add_section('DATABASE')
        config.set('DATABASE', 'database_file', '/home/acserver/stracker/stracker.db3')
        config.set('DATABASE', 'database_type', 'sqlite3')
        config.set('DATABASE', 'perform_backups', 'True')
        config.set('DATABASE', 'postgres_db', 'stracker')
        config.set('DATABASE', 'postgres_host', 'localhost')
        config.set('DATABASE', 'postgres_pwd', 'password')
        config.set('DATABASE', 'postgres_user', 'myuser')

        config.add_section('DB_COMPRESSION')
        config.set('DB_COMPRESSION', 'interval', '60')
        config.set('DB_COMPRESSION', 'mode', 'none')
        config.set('DB_COMPRESSION', 'needs_empty_server', '1')

        config.add_section('HTTP_CONFIG')
        config.set('HTTP_CONFIG', 'admin_password', preset.server_setting.admin_password)
        config.set('HTTP_CONFIG', 'admin_username', 'admin')
        config.set('HTTP_CONFIG', 'auth_log_file', '')
        config.set('HTTP_CONFIG', 'banner', '')
        config.set('HTTP_CONFIG', 'enable_paypal_link', 'True')
        config.set('HTTP_CONFIG', 'enable_svg_generation', 'True')
        config.set('HTTP_CONFIG', 'enabled', 'True')
        config.set('HTTP_CONFIG', 'inverse_navbar', 'False')
        config.set('HTTP_CONFIG', 'items_per_page', '15')
        config.set('HTTP_CONFIG', 'lap_times_add_columns', 'valid+aids+laps+date')
        config.set('HTTP_CONFIG', 'listen_addr', '0.0.0.0')
        config.set('HTTP_CONFIG', 'listen_port', '50041')
        config.set('HTTP_CONFIG', 'log_requests', 'False')
        config.set('HTTP_CONFIG', 'max_streaming_clients', '10')
        config.set('HTTP_CONFIG', 'temperature_unit', 'degc')
        config.set('HTTP_CONFIG', 'velocity_unit', 'kmh')

        config.add_section('BLACKLIST')
        config.set('BLACKLIST', 'blacklist_file', '')

        config.add_section('WELCOME_MSG')
        config.set('WELCOME_MSG', 'line1', 'Welcome to stracker %(version)s')
        config.set('WELCOME_MSG', 'line2', '')
        config.set('WELCOME_MSG', 'line3', '')

        config.add_section('ACPLUGIN')
        config.set('ACPLUGIN', 'proxyPluginLocalPort', '-1')
        config.set('ACPLUGIN', 'proxyPluginPort', '-1')
        config.set('ACPLUGIN', 'rcvPort', '-1')
        config.set('ACPLUGIN', 'sendPort', '-1')

        config.add_section('LAP_VALID_CHECKS')
        config.set('LAP_VALID_CHECKS', 'invalidateOnCarCollisions', 'True')
        config.set('LAP_VALID_CHECKS', 'invalidateOnEnvCollisions', 'True')
        config.set('LAP_VALID_CHECKS', 'ptrackerAllowedTyresOut', '-1')

        config.write(cfg_file, space_around_delimiters=True)
        cfg_file.close()

