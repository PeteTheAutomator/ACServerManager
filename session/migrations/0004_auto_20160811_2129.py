# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0003_auto_20160811_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='name',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='preset',
            name='max_clients',
            field=models.IntegerField(default=None, help_text=b"Maximum number of clients, or leave blank to use the track's number of pitboxes", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='preset',
            name='voting_quorum',
            field=models.IntegerField(default=75, help_text=b'Percentage of vote that is required for the SESSION vote to pass', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
