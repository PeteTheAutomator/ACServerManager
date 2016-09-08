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

    START_RULE_CHOICES = (
        (0, 'Car locked until start'),
        (1, 'Teleport'),
        (2, 'Drivethru'),
    )

    # important stuff
    name = models.CharField(max_length=64, null=True, blank=True, help_text='A brief label to give the preset some context')
    track = models.ForeignKey('library.Track', related_name='track', help_text='The track (and subversion, if any) to race on')
    track_dynamism = models.ForeignKey('library.TrackDynamism', help_text='Track surface conditions')
    max_clients = models.IntegerField(null=True, blank=True, default=None, help_text='Maximum number of clients, or leave blank to use the track\'s number of pitboxes')
    pickup_mode_enabled = models.BooleanField(default=True,
                                              help_text='For sessions that require booking this option must be disabled, otherwise for "first-come-first served" enable this option')
    session_password = models.CharField(max_length=64, null=True, blank=True, default=None, help_text='If you want the session to require a password to join - set that here, otherwise leave blank for a passwordless session')

    # session types
    practice_time = models.IntegerField(default=0, help_text='Time (in minutes) for a Practice session or set to 0 for none')
    practice_is_open = models.BooleanField(default=1)

    qualify_time = models.IntegerField(default=12, help_text='Time (in minutes) for a Qualify session or set to 0 for none')
    qualify_is_open = models.BooleanField(default=1)

    race_laps = models.IntegerField(default=6, help_text='Number of laps for a Race sesion or set to 0 for none')
    race_wait_time = models.IntegerField(default=20, help_text='Seconds to wait before the start of the session')
    race_is_open = models.IntegerField(default=1, choices=RACE_OPEN_CHOICES)
    weathers = models.ManyToManyField('library.Weather')

    # nitty-gritty details
    time_of_day = models.TimeField(default=datetime.time(10, 00), choices=TIME_OF_DAY_CHOICES)
    tc_allowed = models.IntegerField(default=1, choices=ASSIST_CHOICES, help_text='Traction-control')
    abs_allowed = models.IntegerField(default=1, choices=ASSIST_CHOICES, help_text='Anti-lock brakes')
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
    race_over_time = models.IntegerField(default=90)
    loop_mode = models.BooleanField(default=True)
    blacklist_mode = models.IntegerField(choices=BLACKLIST_MODE_CHOICES, default=0)
    qualify_max_wait_perc = models.IntegerField(default=120, help_text='This is the factor to calculate the remaining time in a qualify session after the session is ended: 120 means that 120% of the session fastest lap remains to end the current lap')
    start_rule = models.IntegerField(default=2, choices=START_RULE_CHOICES, help_text='Rules governing race starts / penalties for false-starts. (note: in "Drivethru" mode - if the race has 3 or less laps then the Teleport penalty is enabled)')

    acserver_run_status = models.BooleanField(default=False)
    stracker_run_status = models.BooleanField(default=False)
    minorating_run_status = models.BooleanField(default=False)

    def __unicode__(self):

        if self.name:
            return self.name

        entries = self.entry_set.all()
        car_list = []
        car_list_string_trunc = None
        for entry in entries:
                if entry.car.name not in car_list:
                    car_list.append(entry.car.name)

        if len(car_list) > 0:
            car_list_string = ','.join(car_list)
            car_list_string_trunc = (car_list_string[:40] + '..' if len(car_list_string) > 42 else car_list_string)

        if self.track:
            if len(car_list) > 0:
                return self.track.name + ' (' + car_list_string_trunc + ')'
            else:
                return self.track.name


class Entry(models.Model):
    preset = models.ForeignKey(Preset)
    name = models.CharField(null=True, blank=True, max_length=64)
    car = models.ForeignKey('library.Car')
    skin = ChainedForeignKey(
        'library.CarSkin',
        chained_field="car",
        chained_model_field="car",
        show_all=False,
        auto_choose=True
    )
    fixed_setup = models.BooleanField(default=False, help_text='Apply the stored "Car Setup" (if there is one)')
    spectator_mode = models.BooleanField(default=False)
    team = models.CharField(max_length=64, null=True, blank=True)
    guid = models.CharField(max_length=64, null=True, blank=True)
    ballast = models.IntegerField(default=0)

    def __unicode__(self):
        if self.name:
            return self.car.name + ' (' + self.name + ')'
        else:
            return self.car.name
