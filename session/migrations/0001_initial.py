# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-03 17:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('library', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the preset - this combined with your server-setting name will appear in the Assetto Corsa server listing', max_length=50)),
                ('max_clients', models.IntegerField(default=12, help_text='Maximum number of clients (racers)')),
                ('practice', models.BooleanField(default=1)),
                ('practice_time', models.IntegerField(default=10)),
                ('practice_is_open', models.BooleanField(default=1)),
                ('qualify', models.BooleanField(default=1)),
                ('qualify_time', models.IntegerField(default=10)),
                ('qualify_is_open', models.BooleanField(default=1)),
                ('race', models.BooleanField(default=1)),
                ('race_laps', models.IntegerField(default=5)),
                ('race_wait_time', models.IntegerField(default=10, help_text='Seconds to wait before the start of the session')),
                ('race_is_open', models.IntegerField(choices=[(0, 'no join'), (1, 'free join'), (2, 'close at start')], default=1)),
                ('sun_angle', models.IntegerField(default=48, help_text='Angle of the position of the Sun')),
                ('pickup_mode_enabled', models.BooleanField(default=True, help_text='For sessions that require booking this option must be disabled, otherwise for "first-come-first served" enable this option')),
                ('tc_allowed', models.IntegerField(choices=[(0, 'denied'), (1, 'factory'), (2, 'forced')], default=0, help_text='Traction-control')),
                ('abs_allowed', models.IntegerField(choices=[(0, 'denied'), (1, 'factory'), (2, 'forced')], default=0, help_text='Anti-lock brakes')),
                ('stability_allowed', models.BooleanField(default=0, help_text='Stability-control allowed?')),
                ('autoclutch_allowed', models.BooleanField(default=1, help_text='Automatic clutch allowed?')),
                ('force_virtual_mirror', models.BooleanField(default=0, help_text='Mandatory prominent rear-view mirror?')),
                ('damage_multiplier', models.IntegerField(default=0)),
                ('fuel_rate', models.IntegerField(default=100)),
                ('tyre_blankets_allowed', models.BooleanField(default=1)),
                ('tyre_wear_rate', models.IntegerField(default=100)),
                ('allowed_tyres_out', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=2)),
                ('voting_quorum', models.IntegerField(default=75)),
                ('vote_duration', models.IntegerField(default=20)),
                ('kick_quorum', models.IntegerField(default=85)),
                ('race_over_time', models.IntegerField(default=180)),
                ('loop_mode', models.BooleanField(default=True)),
                ('blacklist_mode', models.IntegerField(choices=[(0, 'normal kick'), (1, 'until server restart'), (2, '??')], default=0)),
                ('cars', models.ManyToManyField(help_text='The models of the cars allowed on the server', to='library.Car')),
                ('server_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.ServerSetting')),
                ('track', models.ForeignKey(help_text='The track (and subversion, if any) to race on', on_delete=django.db.models.deletion.CASCADE, related_name='track', to='library.Track')),
                ('track_dynamism', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.TrackDynamism')),
                ('weathers', models.ManyToManyField(to='library.Weather')),
            ],
        ),
    ]
