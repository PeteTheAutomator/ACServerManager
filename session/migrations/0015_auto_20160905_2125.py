# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0014_auto_20160904_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preset',
            name='name',
            field=models.CharField(help_text=b'A brief label to give the preset some context', max_length=64, null=True, blank=True),
        ),
    ]
