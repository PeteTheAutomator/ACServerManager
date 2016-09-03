# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0009_serversetting_minorating_server_trust_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='serversetting',
            name='proxy_plugin_local_port',
            field=models.IntegerField(default=10004),
        ),
        migrations.AddField(
            model_name='serversetting',
            name='proxy_plugin_port',
            field=models.IntegerField(default=10003),
        ),
    ]
