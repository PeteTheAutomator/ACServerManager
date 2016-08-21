# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preset',
            name='acserver_run_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='preset',
            name='stracker_run_status',
            field=models.BooleanField(default=False),
        ),
    ]
