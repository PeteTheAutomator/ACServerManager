# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0004_auto_20160811_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preset',
            name='sun_angle',
        ),
        migrations.AddField(
            model_name='preset',
            name='time_of_day',
            field=models.TimeField(default=datetime.time(10, 0), choices=[(datetime.time(8, 0), b'08:00'), (datetime.time(9, 0), b'09:00'), (datetime.time(10, 0), b'10:00'), (datetime.time(11, 0), b'11:00'), (datetime.time(12, 0), b'12:00'), (datetime.time(13, 0), b'13:00'), (datetime.time(14, 0), b'14:00'), (datetime.time(15, 0), b'15:00'), (datetime.time(16, 0), b'16:00'), (datetime.time(17, 0), b'17:00'), (datetime.time(18, 0), b'18:00')]),
        ),
    ]
