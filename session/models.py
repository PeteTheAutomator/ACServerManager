from __future__ import unicode_literals

from django.db import models


class Preset(models.Model):
    BLACKLIST_MODE_CHOICES = (
        (0, 'normal kick'),
        (1, 'until server restart'),
        (2, '??'),
    )

    ALLOWED_TYRES_OUT_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

    ASSIST_CHOICES = (
        (0, 'denied'),
        (1, 'factory'),
        (2, 'forced'),
    )

    RACE_OPEN_CHOICES = (
        (0, 'no join'),
        (1, 'free join'),
        (2, 'close at start'),
    )

    # important stuff
    server_setting = models.ForeignKey('library.ServerSetting')
    name = models.CharField(max_length=64, help_text='The name of the preset - this combined with your server-setting name will appear in the Assetto Corsa server listing')
    cars = models.ManyToManyField('library.Car', help_text='The models of the cars allowed on the server')
    track = models.ForeignKey('library.Track', related_name='track', help_text='The track (and subversion, if any) to race on')
    track_dynamism = models.ForeignKey('library.TrackDynamism', null=True, blank=True)
    max_clients = models.IntegerField(default=12, help_text='Maximum number of clients (racers)')

    # session types
    practice = models.BooleanField(default=1)
    practice_time = models.IntegerField(default=10)
    practice_is_open = models.BooleanField(default=1)
    qualify = models.BooleanField(default=1)
    qualify_time = models.IntegerField(default=10)
    qualify_is_open = models.BooleanField(default=1)
    race = models.BooleanField(default=1)
    race_laps = models.IntegerField(default=5)
    race_wait_time = models.IntegerField(default=10, help_text='Seconds to wait before the start of the session')
    race_is_open = models.IntegerField(default=1, choices=RACE_OPEN_CHOICES)
    weathers = models.ManyToManyField('library.Weather')

    # nitty-gritty details
    sun_angle = models.IntegerField(default=48, help_text='Angle of the position of the Sun')
    pickup_mode_enabled = models.BooleanField(default=True, help_text='For sessions that require booking this option must be disabled, otherwise for "first-come-first served" enable this option')
    tc_allowed = models.IntegerField(default=0, choices=ASSIST_CHOICES, help_text='Traction-control')
    abs_allowed = models.IntegerField(default=0, choices=ASSIST_CHOICES, help_text='Anti-lock brakes')
    stability_allowed = models.BooleanField(default=0, help_text='Stability-control allowed?')
    autoclutch_allowed = models.BooleanField(default=1, help_text='Automatic clutch allowed?')
    force_virtual_mirror = models.BooleanField(default=0, help_text='Mandatory prominent rear-view mirror?')
    damage_multiplier = models.IntegerField(default=0)
    fuel_rate = models.IntegerField(default=100)
    tyre_blankets_allowed = models.BooleanField(default=1)
    tyre_wear_rate = models.IntegerField(default=100)
    allowed_tyres_out = models.IntegerField(default=2, choices=ALLOWED_TYRES_OUT_CHOICES)
    voting_quorum = models.IntegerField(default=75)
    vote_duration = models.IntegerField(default=20)
    kick_quorum = models.IntegerField(default=85)
    race_over_time = models.IntegerField(default=180)
    loop_mode = models.BooleanField(default=True)
    blacklist_mode = models.IntegerField(choices=BLACKLIST_MODE_CHOICES, default=0)

    def __unicode__(self):
        return self.server_setting.name + ' - ' + self.name
