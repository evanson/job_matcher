# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20151117_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobmatch',
            name='score',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
