# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0005_auto_20160817_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='preset',
            name='session_password',
            field=models.TextField(default=None, help_text=b'If you want the session to require a password to join - set that here, otherwise leave blank for a passwordless session', null=True, blank=True),
        ),
    ]
