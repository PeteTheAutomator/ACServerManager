# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'assetcollections/%Y/%m/%d')),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
