# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0002_auto_20160821_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serversetting',
            name='client_send_interval',
            field=models.IntegerField(default=20, help_text=b'refresh rate of packet sending by the server. 10Hz = ~100ms. Higher number = higher MP quality = higher bandwidth resources needed. Really high values can create connection issues', verbose_name=b'client send interval (Hz)'),
        ),
    ]
