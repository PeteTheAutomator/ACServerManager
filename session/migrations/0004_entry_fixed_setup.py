# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0003_auto_20160826_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='fixed_setup',
            field=models.BooleanField(default=False, help_text=b'Apply the stored "Car Setup" (if there is one)'),
        ),
    ]
