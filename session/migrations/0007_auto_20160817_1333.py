# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0006_preset_session_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preset',
            name='session_password',
            field=models.CharField(default=None, max_length=64, null=True, help_text=b'If you want the session to require a password to join - set that here, otherwise leave blank for a passwordless session', blank=True),
        ),
    ]
