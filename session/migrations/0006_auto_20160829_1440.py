# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0005_auto_20160829_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preset',
            name='track_dynamism',
            field=models.ForeignKey(default=1, to='library.TrackDynamism', help_text=b'Track surface conditions'),
            preserve_default=False,
        ),
    ]
