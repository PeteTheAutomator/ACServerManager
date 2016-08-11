import os
from configparser import ConfigParser
from background_task import background
from datetime import datetime, timedelta
import subprocess
from django.conf import settings

@background(schedule=timedelta(seconds=10))
def kick_services():
    acserver_return_code = subprocess.call(['/bin/sudo', '/sbin/service', 'acserver', 'restart'])
    if acserver_return_code != 0:
        raise Exception('failed to restart assetto corsa server process')

    stracker_return_code = subprocess.call(['/bin/sudo', '/sbin/service', 'stracker', 'restart'])
    if stracker_return_code != 0:
        raise Exception('failed to restart stracker server process')


class ConfigHandler:
    def __init__(self, config_dir):
        self.config_dir = config_dir

    def write_server_config(self, preset):
        config = ConfigParser()
        config.optionxform = str
        cfg_file = open(os.path.join(self.config_dir, 'server_cfg.ini'), 'w')
        config.add_section('SERVER')

        # build a distinct list of car names
        car_list = []
        for driver in preset.driver_set.all():
            if driver.car.dirname not in car_list:
                car_list.append(driver.car.dirname)

        config.set('SERVER', 'NAME', preset.environment_preset.name)
        config.set('SERVER', 'CARS', ','.join(car_list))
        config.set('SERVER', 'CONFIG_TRACK', '' if not preset.environment_preset.track.subversion else preset.environment_preset.track.subversion)
        config.set('SERVER', 'TRACK', preset.environment_preset.track.dirname)
        config.set('SERVER', 'SUN_ANGLE', str(preset.environment_preset.sun_angle))
        config.set('SERVER', 'PASSWORD', 'TODO')
        config.set('SERVER', 'ADMIN_PASSWORD', 'TODO')
        config.set('SERVER', 'UDP_PORT', str(settings.ASSETTO_CORSA_SERVER_SETTINGS['udp_port']))
        config.set('SERVER', 'TCP_PORT', str(settings.ASSETTO_CORSA_SERVER_SETTINGS['tcp_port']))
        config.set('SERVER', 'HTTP_PORT', str(settings.ASSETTO_CORSA_SERVER_SETTINGS['http_port']))
        config.set('SERVER', 'PICKUP_MODE_ENABLED', str(int(preset.pickup_mode_enabled)))
        config.set('SERVER', 'LOOP_MODE', str(int(preset.environment_preset.loop_mode)))
        config.set('SERVER', 'SLEEP_TIME', '1')
        config.set('SERVER', 'CLIENT_SEND_INTERVAL', str(settings.ASSETTO_CORSA_SERVER_SETTINGS['client_send_interval']))
        config.set('SERVER', 'SEND_BUFFER_SIZE', str(settings.ASSETTO_CORSA_SERVER_SETTINGS['send_buffer_size']))
        config.set('SERVER', 'RECV_BUFFER_SIZE', str(settings.ASSETTO_CORSA_SERVER_SETTINGS['recv_buffer_size']))
        config.set('SERVER', 'RACE_OVER_TIME', str(preset.environment_preset.race_over_time))
        config.set('SERVER', 'KICK_QUORUM', str(preset.environment_preset.kick_quorum))
        config.set('SERVER', 'VOTING_QUORUM', str(preset.environment_preset.voting_quorum))
        config.set('SERVER', 'VOTE_DURATION', str(preset.environment_preset.vote_duration))
        config.set('SERVER', 'BLACKLIST_MODE', str(preset.environment_preset.blacklist_mode))
        config.set('SERVER', 'FUEL_RATE', str(preset.environment_preset.fuel_rate))
        config.set('SERVER', 'DAMAGE_MULTIPLIER', str(preset.environment_preset.damage_multiplier))
        config.set('SERVER', 'TYRE_WEAR_RATE', str(preset.environment_preset.tyre_wear_rate))
        config.set('SERVER', 'ALLOWED_TYRES_OUT', str(preset.environment_preset.allowed_tyres_out))
        config.set('SERVER', 'ABS_ALLOWED', str(preset.environment_preset.abs_allowed))
        config.set('SERVER', 'TC_ALLOWED', str(preset.environment_preset.tc_allowed))
        config.set('SERVER', 'STABILITY_ALLOWED', str(int(preset.environment_preset.stability_allowed)))
        config.set('SERVER', 'AUTOCLUTCH_ALLOWED', str(int(preset.environment_preset.autoclutch_allowed)))
        config.set('SERVER', 'TYRE_BLANKETS_ALLOWED', str(int(preset.environment_preset.tyre_blankets_allowed)))
        config.set('SERVER', 'FORCE_VIRTUAL_MIRROR', str(int(preset.environment_preset.force_virtual_mirror)))
        config.set('SERVER', 'REGISTER_TO_LOBBY', '1')
        config.set('SERVER', 'MAX_CLIENTS', str(preset.environment_preset.max_clients))
        config.set('SERVER', 'UDP_PLUGIN_LOCAL_PORT', '11000')
        config.set('SERVER', 'UDP_PLUGIN_ADDRESS', '127.0.0.1:12000')
        config.set('SERVER', 'AUTH_PLUGIN_ADDRESS', '')
        config.set('SERVER', 'LEGAL_TYRES', 'V;E;HR;ST')

        if preset.environment_preset.practice:
            config.add_section('PRACTICE')
            config.set('PRACTICE', 'NAME', 'Free Practice')
            config.set('PRACTICE', 'TIME', str(preset.environment_preset.practice_time))
            config.set('PRACTICE', 'IS_OPEN', str(int(preset.environment_preset.practice_is_open)))

        if preset.environment_preset.qualify:
            config.add_section('QUALIFY')
            config.set('QUALIFY', 'NAME', 'Qualify')
            config.set('QUALIFY', 'TIME', str(preset.environment_preset.qualify_time))
            config.set('QUALIFY', 'IS_OPEN', str(int(preset.environment_preset.qualify_is_open)))

        if preset.environment_preset.race:
            config.add_section('RACE')
            config.set('RACE', 'NAME', 'Race')
            config.set('RACE', 'LAPS', str(preset.environment_preset.race_laps))
            config.set('RACE', 'WAIT_TIME', str(preset.environment_preset.race_wait_time))
            config.set('RACE', 'IS_OPEN', str(preset.environment_preset.race_is_open))

        if preset.environment_preset.track_dynamism:
            config.add_section('DYNAMIC_TRACK')
            config.set('DYNAMIC_TRACK', 'SESSION_START', str(preset.environment_preset.track_dynamism.session_start))
            config.set('DYNAMIC_TRACK', 'RANDOMNESS', str(preset.environment_preset.track_dynamism.randomness))
            config.set('DYNAMIC_TRACK', 'SESSION_TRANSFER', str(preset.environment_preset.track_dynamism.session_transfer))
            config.set('DYNAMIC_TRACK', 'LAP_GAIN', str(preset.environment_preset.track_dynamism.lap_gain))

        weather_count = 0
        for weather in preset.environment_preset.weathers.all():
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

        for driver in preset.driver_set.all():
            car_section = 'CAR_' + str(car_count)
            config.add_section(car_section)
            config.set(car_section, 'MODEL', driver.car.dirname)
            config.set(car_section, 'SKIN', 'TODO')
            config.set(car_section, 'SPECTATOR_MODE', str(int(driver.spectator_mode)))
            config.set(car_section, 'DRIVER_NAME', driver.name)
            config.set(car_section, 'TEAM', driver.team)
            config.set(car_section, 'GUID', driver.guid)
            config.set(car_section, 'BALLAST', str(driver.ballast))
            car_count += 1

        config.write(cfg_file, space_around_delimiters=False)
        cfg_file.close()
