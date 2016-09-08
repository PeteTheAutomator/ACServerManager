# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0015_auto_20160905_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preset',
            name='server_setting',
        ),
        migrations.DeleteModel(
            name='ServerSetting',
        ),
    ]
