# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_skills', '0002_auto_20151117_1344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobskill',
            options={'ordering': ['name']},
        ),
    ]
