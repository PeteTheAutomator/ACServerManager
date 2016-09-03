# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0010_auto_20160903_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='preset',
            name='minorating_run_status',
            field=models.BooleanField(default=False),
        ),
    ]
