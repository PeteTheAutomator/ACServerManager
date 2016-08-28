# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20160825_1001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['name'], 'verbose_name': 'Car Setup'},
        ),
        migrations.AddField(
            model_name='car',
            name='fixed_setup',
            field=models.TextField(help_text=b'Store a fixed setup here if you wish; the contents can be copied from "Documents\\Assetto Corsa\\setups\\<car>\\<track>\\<setup-name>.ini", and pasted here.  If you check the "fixed setup" option in your Preset\'s Entries - this fixed setup is applied', null=True, blank=True),
        ),
    ]
