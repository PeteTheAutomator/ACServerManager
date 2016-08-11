# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('spectator_mode', models.BooleanField(default=False)),
                ('team', models.CharField(max_length=64, null=True, blank=True)),
                ('guid', models.CharField(max_length=64, null=True, blank=True)),
                ('ballast', models.IntegerField(default=0)),
                ('car', models.ForeignKey(to='library.Car')),
            ],
        ),
        migrations.CreateModel(
            name='EntryGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('pickup_mode_enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of the preset - this will appear in the Assetto Corsa server listing', max_length=64)),
                ('welcome_message', models.TextField(default=b'Welcome!')),
                ('max_clients', models.IntegerField(default=12, help_text=b'Maximum number of clients (racers)')),
                ('practice', models.BooleanField(default=1)),
                ('practice_time', models.IntegerField(default=10)),
                ('practice_is_open', models.BooleanField(default=1)),
                ('qualify', models.BooleanField(default=1)),
                ('qualify_time', models.IntegerField(default=10)),
                ('qualify_is_open', models.BooleanField(default=1)),
                ('race', models.BooleanField(default=1)),
                ('race_laps', models.IntegerField(default=5)),
                ('race_wait_time', models.IntegerField(default=10, help_text=b'Seconds to wait before the start of the session')),
                ('race_is_open', models.IntegerField(default=1, choices=[(0, b'no join'), (1, b'free join'), (2, b'close at start')])),
                ('sun_angle', models.IntegerField(default=48, help_text=b'Angle of the position of the Sun')),
                ('tc_allowed', models.IntegerField(default=0, help_text=b'Traction-control', choices=[(0, b'denied'), (1, b'factory'), (2, b'forced')])),
                ('abs_allowed', models.IntegerField(default=0, help_text=b'Anti-lock brakes', choices=[(0, b'denied'), (1, b'factory'), (2, b'forced')])),
                ('stability_allowed', models.BooleanField(default=0, help_text=b'Stability-control allowed?')),
                ('autoclutch_allowed', models.BooleanField(default=1, help_text=b'Automatic clutch allowed?')),
                ('force_virtual_mirror', models.BooleanField(default=0, help_text=b'Mandatory prominent rear-view mirror?')),
                ('damage_multiplier', models.IntegerField(default=0)),
                ('fuel_rate', models.IntegerField(default=100)),
                ('tyre_blankets_allowed', models.BooleanField(default=1)),
                ('tyre_wear_rate', models.IntegerField(default=100)),
                ('allowed_tyres_out', models.IntegerField(default=2, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])),
                ('voting_quorum', models.IntegerField(default=75)),
                ('vote_duration', models.IntegerField(default=20)),
                ('kick_quorum', models.IntegerField(default=85)),
                ('race_over_time', models.IntegerField(default=180)),
                ('loop_mode', models.BooleanField(default=True)),
                ('blacklist_mode', models.IntegerField(default=0, choices=[(0, b'normal kick'), (1, b'until server restart'), (2, b'??')])),
                ('track', models.ForeignKey(related_name='track', to='library.Track', help_text=b'The track (and subversion, if any) to race on')),
                ('track_dynamism', models.ForeignKey(blank=True, to='library.TrackDynamism', null=True)),
                ('weathers', models.ManyToManyField(to='library.Weather')),
            ],
        ),
        migrations.AddField(
            model_name='entrygroup',
            name='environment_preset',
            field=models.ForeignKey(to='session.Environment'),
        ),
        migrations.AddField(
            model_name='entry',
            name='driver_preset',
            field=models.ForeignKey(to='session.EntryGroup'),
        ),
    ]
