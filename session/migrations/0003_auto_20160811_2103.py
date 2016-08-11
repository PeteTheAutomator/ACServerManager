# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0002_auto_20160811_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preset',
            name='max_clients',
            field=models.IntegerField(default=None, help_text=b'Maximum number of clients (racers)', null=True, blank=True),
        ),
    ]
