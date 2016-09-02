# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0007_auto_20160829_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='preset',
            name='qualify_max_wait_perc',
            field=models.IntegerField(default=120, help_text=b'This is the factor to calculate the remaining time in a qualify session after the session is ended: 120 means that 120% of the session fastest lap remains to end the current lap'),
        ),
        migrations.AddField(
            model_name='preset',
            name='start_rule',
            field=models.IntegerField(default=2, help_text=b'Rules governing race starts / penalties for false-starts. (note: in "Drivethru" mode - if the race has 3 or less laps then the Teleport penalty is enabled)', choices=[(0, b'Car locked until start'), (1, b'Teleport'), (2, b'Drivethru')]),
        ),
        migrations.AlterField(
            model_name='preset',
            name='abs_allowed',
            field=models.IntegerField(default=1, help_text=b'Anti-lock brakes', choices=[(0, b'denied'), (1, b'factory'), (2, b'forced')]),
        ),
        migrations.AlterField(
            model_name='preset',
            name='race_over_time',
            field=models.IntegerField(default=90),
        ),
        migrations.AlterField(
            model_name='preset',
            name='race_wait_time',
            field=models.IntegerField(default=20, help_text=b'Seconds to wait before the start of the session'),
        ),
        migrations.AlterField(
            model_name='preset',
            name='tc_allowed',
            field=models.IntegerField(default=1, help_text=b'Traction-control', choices=[(0, b'denied'), (1, b'factory'), (2, b'forced')]),
        ),
    ]
