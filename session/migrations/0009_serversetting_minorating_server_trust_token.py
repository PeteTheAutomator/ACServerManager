# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0008_auto_20160902_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='serversetting',
            name='minorating_server_trust_token',
            field=models.CharField(max_length=48, null=True, verbose_name=b'Unique server token for MinoRating', blank=True),
        ),
    ]
