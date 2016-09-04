# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0013_auto_20160904_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serversetting',
            name='minorating_grade',
            field=models.CharField(default=b'ABCN', help_text=b"Minorating Grade required to join this server's sessions (driver proficiency - see http://www.minorating.com/Grades for details)", max_length=8, choices=[(b'A', b'A - exemplary'), (b'AB', b'AB - clean racer (or better)'), (b'ABC', b'ABC - rookie (or better)'), (b'ABCN', b'ABCN - rookie or new/unlisted racers (or better)'), (b'ABCDN', b'ABCDN - dirty racers welcome'), (b'ABCDNW', b'ABCDNW - anybody (including wreckers)')]),
        ),
    ]
