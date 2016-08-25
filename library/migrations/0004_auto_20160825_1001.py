# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20160825_0956'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assetcollection',
            old_name='docfile',
            new_name='collection',
        ),
    ]
