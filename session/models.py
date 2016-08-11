from django.db import models
from library.models import Car

class Environment(models.Model):
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
    name = models.CharField(max_length=64, help_text='The name of the preset - this will appear in the Assetto Corsa server listing')
    welcome_message = models.TextField(default='Welcome!')
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
        return self.name


class EntryGroup(models.Model):
    environment_preset = models.ForeignKey(Environment)
    name = models.CharField(max_length=64)
    pickup_mode_enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def auto_populate(self, tag):
        if self.environment_preset:
            num_entries = self.environment_preset.track.pitboxes
            entry_counter = 0

            cars = Car.objects.filter(tags=tag)
            car_iterator = 0

            while entry_counter < num_entries:
                Entry.objects.create(
                    driver_preset=self,
                    name='CAR_' + str(entry_counter),
                    car=cars[car_iterator],
                )
                entry_counter += 1
                car_iterator += 1
                if car_iterator > len(cars):
                    car_iterator = 0

class Entry(models.Model):
    driver_preset = models.ForeignKey(EntryGroup)
    name = models.CharField(max_length=64)
    car = models.ForeignKey('library.Car')
    #skin = models.ForeignKey('library.Car.carskin')
    spectator_mode = models.BooleanField(default=False)
    team = models.CharField(max_length=64, null=True, blank=True)
    guid = models.CharField(max_length=64, null=True, blank=True)
    ballast = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name
