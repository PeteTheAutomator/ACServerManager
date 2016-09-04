# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0011_preset_minorating_run_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='serversetting',
            name='minorating_grade',
            field=models.CharField(default=b'ABCN', help_text=b"Minorating Grade required to join this server's sessions (driver proficiency - see http://www.minorating.com/Grades for details)", max_length=8, choices=[(b'A', b'A - exemplary'), (b'AB', b'AB - clean racer (or better)'), (b'ABC', b'ABC - rookie (or better)'), (b'ABCN', b'ABCN - new/unlisted racers (or better)'), (b'ABCNW', b'ABCNW - anybody (including wreckers)')]),
        ),
        migrations.AlterField(
            model_name='serversetting',
            name='minorating_server_trust_token',
            field=models.CharField(help_text=b'this value is initialised when the server contacts Minorating for the first time; you may wish to record this value if migrating to another server', max_length=48, null=True, verbose_name=b'Unique server token for MinoRating', blank=True),
        ),
    ]
