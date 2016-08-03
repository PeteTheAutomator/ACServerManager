import ConfigParser


class ConfigHandler:
    def __init__(self):
        self.Config = ConfigParser.ConfigParser()
        self.Config.optionxform = str

    def write_config(self, preset):
        cfgfile = open('/var/tmp/woo.conf', 'w')
        self.Config.add_section('SERVER')
        self.Config.set('SERVER', 'NAME', preset.server_setting.name + ' - ' + preset.name)
        self.Config.set('SERVER', 'CARS', ','.join([car.name for car in preset.cars.all()]))
        self.Config.set('SERVER', 'CONFIG_TRACK', '' if not preset.track.subversion else preset.track.subversion)
        self.Config.set('SERVER', 'TRACK', preset.track.name)
        self.Config.set('SERVER', 'SUN_ANGLE', preset.sun_angle)
        self.Config.set('SERVER', 'PASSWORD', 'TODO')
        self.Config.set('SERVER', 'ADMIN_PASSWORD', 'TODO')
        self.Config.set('SERVER', 'UDP_PORT', preset.server_setting.udp_port)
        self.Config.set('SERVER', 'TCP_PORT', preset.server_setting.tcp_port)
        self.Config.set('SERVER', 'HTTP_PORT', preset.server_setting.http_port)
        self.Config.set('SERVER', 'PICKUP_MODE_ENABLED', int(preset.pickup_mode_enabled))
        self.Config.set('SERVER', 'LOOP_MODE', int(preset.loop_mode))
        self.Config.set('SERVER', 'SLEEP_TIME', '1')
        self.Config.set('SERVER', 'CLIENT_SEND_INTERVAL', preset.server_setting.client_send_interval)
        self.Config.set('SERVER', 'SEND_BUFFER_SIZE', preset.server_setting.send_buffer_size)
        self.Config.set('SERVER', 'RECV_BUFFER_SIZE', preset.server_setting.recv_buffer_size)
        self.Config.set('SERVER', 'RACE_OVER_TIME', preset.race_over_time)
        self.Config.set('SERVER', 'KICK_QUORUM', preset.kick_quorum)
        self.Config.set('SERVER', 'VOTING_QUORUM', preset.voting_quorum)
        self.Config.set('SERVER', 'VOTE_DURATION', preset.vote_duration)
        self.Config.set('SERVER', 'BLACKLIST_MODE', preset.blacklist_mode)
        self.Config.set('SERVER', 'FUEL_RATE', preset.fuel_rate)
        self.Config.set('SERVER', 'DAMAGE_MULTIPLIER', preset.damage_multiplier)
        self.Config.set('SERVER', 'TYRE_WEAR_RATE', preset.tyre_wear_rate)
        self.Config.set('SERVER', 'ALLOWED_TYRES_OUT', preset.allowed_tyres_out)
        self.Config.set('SERVER', 'ABS_ALLOWED', preset.abs_allowed)
        self.Config.set('SERVER', 'TC_ALLOWED', preset.tc_allowed)
        self.Config.set('SERVER', 'STABILITY_ALLOWED', int(preset.stability_allowed))
        self.Config.set('SERVER', 'AUTOCLUTCH_ALLOWED', int(preset.autoclutch_allowed))
        self.Config.set('SERVER', 'TYRE_BLANKETS_ALLOWED', int(preset.tyre_blankets_allowed))
        self.Config.set('SERVER', 'FORCE_VIRTUAL_MIRROR', int(preset.force_virtual_mirror))
        self.Config.set('SERVER', 'REGISTER_TO_LOBBY', '1')
        self.Config.set('SERVER', 'MAX_CLIENTS', preset.max_clients)
        self.Config.set('SERVER', 'UDP_PLUGIN_LOCAL_PORT', '0')
        self.Config.set('SERVER', 'UDP_PLUGIN_ADDRESS', '')
        self.Config.set('SERVER', 'AUTH_PLUGIN_ADDRESS', '')
        self.Config.set('SERVER', 'LEGAL_TYRES', 'V;E;HR;ST')

        if preset.practice:
            self.Config.add_section('PRACTICE')
            self.Config.set('PRACTICE', 'NAME', 'Free Practice')
            self.Config.set('PRACTICE', 'TIME', preset.practice_time)
            self.Config.set('PRACTICE', 'IS_OPEN', int(preset.practice_is_open))

        if preset.qualify:
            self.Config.add_section('QUALIFY')
            self.Config.set('QUALIFY', 'NAME', 'Qualify')
            self.Config.set('QUALIFY', 'TIME', preset.qualify_time)
            self.Config.set('QUALIFY', 'IS_OPEN', int(preset.qualify_is_open))

        if preset.race:
            self.Config.add_section('RACE')
            self.Config.set('RACE', 'NAME', 'Race')
            self.Config.set('RACE', 'LAPS', preset.race_laps)
            self.Config.set('RACE', 'WAIT_TIME', preset.race_wait_time)
            self.Config.set('RACE', 'IS_OPEN', preset.race_is_open)

        if preset.track_dynamism:
            self.Config.add_section('DYNAMIC_TRACK')
            self.Config.set('DYNAMIC_TRACK', 'SESSION_START', preset.track_dynamism.session_start)
            self.Config.set('DYNAMIC_TRACK', 'RANDOMNESS', preset.track_dynamism.randomness)
            self.Config.set('DYNAMIC_TRACK', 'SESSION_TRANSFER', preset.track_dynamism.session_transfer)
            self.Config.set('DYNAMIC_TRACK', 'LAP_GAIN', preset.track_dynamism.lap_gain)

        weather_count = 0
        for weather in preset.weathers.all():
            weather_section = 'WEATHER_' + str(weather_count)
            self.Config.add_section(weather_section)
            self.Config.set(weather_section, 'GRAPHICS', weather.graphics)
            self.Config.set(weather_section, 'BASE_TEMPERATURE_AMBIENT', weather.base_temperature_ambient)
            self.Config.set(weather_section, 'VARIATION_AMBIENT', weather.variation_ambient)
            self.Config.set(weather_section, 'BASE_TEMPERATURE_ROAD', weather.base_temperature_road)
            self.Config.set(weather_section, 'VARIATION_ROAD', weather.variation_road)
            weather_count += 1

        self.Config.write(cfgfile)
        cfgfile.close()
