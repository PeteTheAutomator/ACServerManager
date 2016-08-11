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
                ('brand', models.CharField(max_length=64)),
                ('clarse', models.CharField(max_length=64, verbose_name=b'class')),
                ('dirname', models.CharField(max_length=64)),
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
            name='CarTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('dirname', models.CharField(max_length=64)),
                ('subversion', models.CharField(max_length=64, null=True, blank=True)),
                ('run', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('pitboxes', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=128)),
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
                ('realistic_road_temp', models.IntegerField(default=7, verbose_name=b'realistic road temperature')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='tags',
            field=models.ManyToManyField(to='library.CarTag'),
        ),
    ]
