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
    config_dir = os.path.join(settings.ACSERVER_CONFIG_DIR, preset_id)
    ch = ConfigHandler(config_dir)
    ch.write_server_config(preset)
    ch.write_entries_config(preset)
    ch.write_welcome_message(preset)


@background(schedule=timedelta(seconds=1))
def kick_services():
    p = Popen(['/bin/sudo', '/usr/bin/systemctl', 'restart', 'acserver'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.communicate()
    acserver_return_code = p.returncode

    if acserver_return_code != 0:
        raise Exception('failed to restart assetto corsa server process')

    p = Popen(['/bin/sudo', '/usr/bin/systemctl', 'restart', 'stracker'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.communicate()
    stracker_return_code = p.returncode
    if stracker_return_code != 0:
        raise Exception('failed to restart stracker server process')


def get_server_status():
    p = Popen(['/bin/sudo', '/usr/bin/systemctl', 'list-units'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    server_status_dict = {}
    if rc == 0:
        output_lines = output.split('\n')
        for preset in Preset.objects.all():
            server_status_dict[preset.id] = False
            acserver_regex = re.compile('\s*acserver@' + str(preset.id) + '\.service\s+loaded active running')
            for line in output_lines:
                if re.match(acserver_regex, line):
                    server_status_dict[preset.id] = True
    return server_status_dict
        

def time_to_sun_angle(time):
    return str((time.hour - 13) * 16)


class ConfigHandler:
    def __init__(self, config_dir):
        self.config_dir = config_dir
        if not os.path.isdir(self.config_dir):
            os.makedirs(self.config_dir)

    def write_server_config(self, preset):
        config = ConfigParser()
        config.optionxform = str
        cfg_file = open(os.path.join(self.config_dir, 'server_cfg.ini'), 'w')
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
            config.set('SERVER', 'WELCOME_MESSAGE', str(os.path.join(self.config_dir, 'welcome_message.txt')))

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
        cfg_file = open(os.path.join(self.config_dir, 'entry_list.ini'), 'w')
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
        fh = open(os.path.join(self.config_dir, 'welcome_message.txt'), 'w')
        fh.write(preset.server_setting.welcome_message)
        fh.close()

