# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_skills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=60)),
                ('address', models.CharField(max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.SlugField(choices=[(b'accounting', b'Accounting & Finance'), (b'administration', b'Administration'), (b'agriculture', b'Agriculture'), (b'architecture', b'Architecture'), (b'audit', b'Auditing & Risk Management'), (b'banking', b'Banking & Investment'), (b'business_administration', b'Business administration & management'), (b'communication', b'Communication & Public Relations'), (b'community_development', b'Community Development & Social Work'), (b'customer_service', b'Customer Service'), (b'design', b'Design'), (b'education', b'Education & teaching'), (b'engineering', b'Engineering'), (b'health', b'Health & Medical Services'), (b'hospitality', b'Hospitality'), (b'IT', b'IT'), (b'legal', b'Legal Services'), (b'media', b'Media & Journalism'), (b'project_management', b'Project Management'), (b'sales_marketing', b'Sales & Marketing')])),
                ('summary', models.CharField(max_length=500, verbose_name=b'A brief summary of who you are & your capabilities')),
                ('years_of_experience', models.IntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobSeekerSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seeker', models.ForeignKey(to='accounts.JobSeeker')),
                ('skill', models.ForeignKey(to='job_skills.JobSkill')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.SlugField(choices=[(b'admin', b'Admin'), (b'job_seeker', b'Job Seeker'), (b'employer', b'Employer')])),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
