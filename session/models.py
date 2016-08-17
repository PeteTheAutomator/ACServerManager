from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from smart_selects.db_fields import ChainedForeignKey
import datetime


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

    TIME_OF_DAY_CHOICES = (
        (datetime.time(8), '08:00'),
        (datetime.time(9), '09:00'),
        (datetime.time(10), '10:00'),
        (datetime.time(11), '11:00'),
        (datetime.time(12), '12:00'),
        (datetime.time(13), '13:00'),
        (datetime.time(14), '14:00'),
        (datetime.time(15), '15:00'),
        (datetime.time(16), '16:00'),
        (datetime.time(17), '17:00'),
        (datetime.time(18), '18:00'),
    )

    # important stuff
    name = models.CharField(max_length=64, help_text='The name of the preset - this will appear in the Assetto Corsa server listing')
    welcome_message = models.TextField(default='Welcome!')
    track = models.ForeignKey('library.Track', related_name='track', help_text='The track (and subversion, if any) to race on')
    track_dynamism = models.ForeignKey('library.TrackDynamism', null=True, blank=True)
    max_clients = models.IntegerField(null=True, blank=True, default=None, help_text='Maximum number of clients, or leave blank to use the track\'s number of pitboxes')
    pickup_mode_enabled = models.BooleanField(default=True,
                                              help_text='For sessions that require booking this option must be disabled, otherwise for "first-come-first served" enable this option')
    session_password = models.TextField(null=True, blank=True, default=None, help_text='If you want the session to require a password to join - set that here, otherwise leave blank for a passwordless session')

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
    time_of_day = models.TimeField(default=datetime.time(10, 00), choices=TIME_OF_DAY_CHOICES)
    tc_allowed = models.IntegerField(default=0, choices=ASSIST_CHOICES, help_text='Traction-control')
    abs_allowed = models.IntegerField(default=0, choices=ASSIST_CHOICES, help_text='Anti-lock brakes')
    stability_allowed = models.BooleanField(default=0, help_text='Stability-control allowed?')
    autoclutch_allowed = models.BooleanField(default=1, help_text='Automatic clutch allowed?')
    force_virtual_mirror = models.BooleanField(default=0, help_text='Mandatory prominent rear-view mirror?')
    damage_multiplier = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Damage from 0 (no damage) to 100 (full damage)')
    fuel_rate = models.IntegerField(default=100)
    tyre_blankets_allowed = models.BooleanField(default=1)
    tyre_wear_rate = models.IntegerField(default=100)
    allowed_tyres_out = models.IntegerField(default=2, choices=ALLOWED_TYRES_OUT_CHOICES)
    voting_quorum = models.IntegerField(default=75, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Percentage of vote that is required for the SESSION vote to pass')
    vote_duration = models.IntegerField(default=20)
    kick_quorum = models.IntegerField(default=85)
    race_over_time = models.IntegerField(default=180)
    loop_mode = models.BooleanField(default=True)
    blacklist_mode = models.IntegerField(choices=BLACKLIST_MODE_CHOICES, default=0)

    def __unicode__(self):
        return self.name + ' / ' + self.track.name


class Entry(models.Model):
    environment = models.ForeignKey(Preset)
    name = models.CharField(null=True, blank=True, max_length=64)
    car = models.ForeignKey('library.Car')
    skin = ChainedForeignKey(
        'library.CarSkin',
        chained_field="car",
        chained_model_field="car",
        show_all=False,
        auto_choose=True
    )
    spectator_mode = models.BooleanField(default=False)
    team = models.CharField(max_length=64, null=True, blank=True)
    guid = models.CharField(max_length=64, null=True, blank=True)
    ballast = models.IntegerField(default=0)

    def __unicode__(self):
        if self.name:
            return self.car.name + ' (' + self.name + ')'
        else:
            return self.car.name
