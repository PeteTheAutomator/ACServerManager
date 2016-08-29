# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0006_auto_20160829_1440'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='environment',
            new_name='preset',
        ),
    ]
