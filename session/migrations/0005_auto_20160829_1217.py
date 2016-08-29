# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0004_entry_fixed_setup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preset',
            name='practice',
        ),
        migrations.RemoveField(
            model_name='preset',
            name='qualify',
        ),
        migrations.RemoveField(
            model_name='preset',
            name='race',
        ),
        migrations.AlterField(
            model_name='preset',
            name='practice_time',
            field=models.IntegerField(default=0, help_text=b'Time (in minutes) for a Practice session or set to 0 for none'),
        ),
        migrations.AlterField(
            model_name='preset',
            name='qualify_time',
            field=models.IntegerField(default=12, help_text=b'Time (in minutes) for a Qualify session or set to 0 for none'),
        ),
        migrations.AlterField(
            model_name='preset',
            name='race_laps',
            field=models.IntegerField(default=6, help_text=b'Number of laps for a Race sesion or set to 0 for none'),
        ),
    ]
