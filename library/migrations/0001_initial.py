# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CarSkin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('car', models.ForeignKey(to='library.Car')),
            ],
        ),
        migrations.CreateModel(
            name='ServerSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'A common name for your server - this forms a prefix in the Assetto Corsa server listing, followed-by the running race-preset name', max_length=64)),
                ('welcome_message', models.TextField(default=b'Welcome!')),
                ('udp_port', models.IntegerField(default=9600, help_text=b'UDP port number which the ACServer binds to')),
                ('tcp_port', models.IntegerField(default=9600, help_text=b'TCP port number which the ACServer binds to')),
                ('http_port', models.IntegerField(default=8081, help_text=b'HTTP port number which Lobby binds to')),
                ('send_buffer_size', models.IntegerField(default=0)),
                ('recv_buffer_size', models.IntegerField(default=0)),
                ('client_send_interval', models.IntegerField(default=15)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('subversion', models.CharField(max_length=64, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrackDynamism',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('session_start', models.IntegerField()),
                ('randomness', models.IntegerField()),
                ('session_transfer', models.IntegerField()),
                ('lap_gain', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('graphics', models.CharField(max_length=64)),
                ('base_temperature_ambient', models.IntegerField(default=20, verbose_name=b'base ambient temperature')),
                ('variation_ambient', models.IntegerField(default=2, verbose_name=b'ambient variation')),
                ('base_temperature_road', models.IntegerField(default=7, verbose_name=b'base road temperature')),
                ('variation_road', models.IntegerField(default=2, verbose_name=b'road variation')),
            ],
        ),
    ]
