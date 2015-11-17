# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.SlugField(choices=[(b'accounting', b'Accounting & Finance'), (b'administration', b'Administration'), (b'agriculture', b'Agriculture'), (b'architecture', b'Architecture'), (b'audit', b'Auditing & Risk Management'), (b'banking', b'Banking & Investment'), (b'business_administration', b'Business administration & management'), (b'communication', b'Communication & Public Relations'), (b'community_development', b'Community Development & Social Work'), (b'customer_service', b'Customer Service'), (b'design', b'Design'), (b'education', b'Education & teaching'), (b'engineering', b'Engineering'), (b'health', b'Health & Medical Services'), (b'hospitality', b'Hospitality'), (b'IT', b'IT'), (b'legal', b'Legal Services'), (b'media', b'Media & Journalism'), (b'project_management', b'Project Management'), (b'sales_marketing', b'Sales & Marketing')])),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='jobskill',
            unique_together=set([('category', 'name')]),
        ),
    ]
