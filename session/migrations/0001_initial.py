# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, null=True, blank=True)),
                ('spectator_mode', models.BooleanField(default=False)),
                ('team', models.CharField(max_length=64, null=True, blank=True)),
                ('guid', models.CharField(max_length=64, null=True, blank=True)),
                ('ballast', models.IntegerField(default=0)),
                ('car', models.ForeignKey(to='library.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Preset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'A brief label to give the preset some context', max_length=64)),
                ('max_clients', models.IntegerField(default=None, help_text=b"Maximum number of clients, or leave blank to use the track's number of pitboxes", null=True, blank=True)),
                ('pickup_mode_enabled', models.BooleanField(default=True, help_text=b'For sessions that require booking this option must be disabled, otherwise for "first-come-first served" enable this option')),
                ('session_password', models.CharField(default=None, max_length=64, null=True, help_text=b'If you want the session to require a password to join - set that here, otherwise leave blank for a passwordless session', blank=True)),
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
                ('time_of_day', models.TimeField(default=datetime.time(10, 0), choices=[(datetime.time(8, 0), b'08:00'), (datetime.time(9, 0), b'09:00'), (datetime.time(10, 0), b'10:00'), (datetime.time(11, 0), b'11:00'), (datetime.time(12, 0), b'12:00'), (datetime.time(13, 0), b'13:00'), (datetime.time(14, 0), b'14:00'), (datetime.time(15, 0), b'15:00'), (datetime.time(16, 0), b'16:00'), (datetime.time(17, 0), b'17:00'), (datetime.time(18, 0), b'18:00')])),
                ('tc_allowed', models.IntegerField(default=0, help_text=b'Traction-control', choices=[(0, b'denied'), (1, b'factory'), (2, b'forced')])),
                ('abs_allowed', models.IntegerField(default=0, help_text=b'Anti-lock brakes', choices=[(0, b'denied'), (1, b'factory'), (2, b'forced')])),
                ('stability_allowed', models.BooleanField(default=0, help_text=b'Stability-control allowed?')),
                ('autoclutch_allowed', models.BooleanField(default=1, help_text=b'Automatic clutch allowed?')),
                ('force_virtual_mirror', models.BooleanField(default=0, help_text=b'Mandatory prominent rear-view mirror?')),
                ('damage_multiplier', models.IntegerField(default=100, help_text=b'Damage from 0 (no damage) to 100 (full damage)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('fuel_rate', models.IntegerField(default=100)),
                ('tyre_blankets_allowed', models.BooleanField(default=1)),
                ('tyre_wear_rate', models.IntegerField(default=100)),
                ('allowed_tyres_out', models.IntegerField(default=2, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])),
                ('voting_quorum', models.IntegerField(default=75, help_text=b'Percentage of vote that is required for the SESSION vote to pass', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('vote_duration', models.IntegerField(default=20)),
                ('kick_quorum', models.IntegerField(default=85)),
                ('race_over_time', models.IntegerField(default=180)),
                ('loop_mode', models.BooleanField(default=True)),
                ('blacklist_mode', models.IntegerField(default=0, choices=[(0, b'normal kick'), (1, b'until server restart'), (2, b'??')])),
            ],
        ),
        migrations.CreateModel(
            name='ServerSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b"The name of the server - this will appear in the Assetto Corsa's listing of online servers for the public to join", max_length=64)),
                ('welcome_message', models.TextField(help_text=b'Place a welcome message here - this will display some dialog to clients upon joining a session which they must click to close', null=True, blank=True)),
                ('udp_port', models.IntegerField(default=9600, help_text=b'Assetto Corsa server UDP port number')),
                ('tcp_port', models.IntegerField(default=9600, help_text=b'Assetto Corser server TCP port number')),
                ('http_port', models.IntegerField(default=8081, help_text=b'Lobby port number')),
                ('send_buffer_size', models.IntegerField(default=0, help_text=b'DOCUMENTATION SOURCE NEEDED')),
                ('recv_buffer_size', models.IntegerField(default=0, help_text=b'DOCUMENTATION SOURCE NEEDED')),
                ('client_send_interval', models.IntegerField(default=15, help_text=b'refresh rate of packet sending by the server. 10Hz = ~100ms. Higher number = higher MP quality = higher bandwidth resources needed. Really high values can create connection issues', verbose_name=b'client send interval (Hz)')),
            ],
        ),
        migrations.AddField(
            model_name='preset',
            name='server_setting',
            field=models.ForeignKey(to='session.ServerSetting'),
        ),
        migrations.AddField(
            model_name='preset',
            name='track',
            field=models.ForeignKey(related_name='track', to='library.Track', help_text=b'The track (and subversion, if any) to race on'),
        ),
        migrations.AddField(
            model_name='preset',
            name='track_dynamism',
            field=models.ForeignKey(blank=True, to='library.TrackDynamism', null=True),
        ),
        migrations.AddField(
            model_name='preset',
            name='weathers',
            field=models.ManyToManyField(to='library.Weather'),
        ),
        migrations.AddField(
            model_name='entry',
            name='environment',
            field=models.ForeignKey(to='session.Preset'),
        ),
        migrations.AddField(
            model_name='entry',
            name='skin',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'car', chained_field=b'car', auto_choose=True, to='library.CarSkin'),
        ),
    ]
