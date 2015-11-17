# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('job_skills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=600, verbose_name=b'Description of the responsibilities for the job')),
                ('category', models.SlugField(choices=[(b'accounting', b'Accounting & Finance'), (b'administration', b'Administration'), (b'agriculture', b'Agriculture'), (b'architecture', b'Architecture'), (b'audit', b'Auditing & Risk Management'), (b'banking', b'Banking & Investment'), (b'business_administration', b'Business administration & management'), (b'communication', b'Communication & Public Relations'), (b'community_development', b'Community Development & Social Work'), (b'customer_service', b'Customer Service'), (b'design', b'Design'), (b'education', b'Education & teaching'), (b'engineering', b'Engineering'), (b'health', b'Health & Medical Services'), (b'hospitality', b'Hospitality'), (b'IT', b'IT'), (b'legal', b'Legal Services'), (b'media', b'Media & Journalism'), (b'project_management', b'Project Management'), (b'sales_marketing', b'Sales & Marketing')])),
                ('years_of_experience', models.IntegerField(verbose_name=b'Minimum years of experience required')),
                ('other', models.CharField(max_length=600, verbose_name=b'Additional Information')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(to='accounts.Employer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.SlugField(choices=[(b'strong', b'Strong Match'), (b'exact', b'Exact Match'), (b'weak', b'Weak Match')])),
                ('notification_sent', models.BooleanField(default=False)),
                ('status', models.SlugField(default=b'interested', choices=[(b'interested', b'Interested'), (b'not_interested', b'Not Interested')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(to='jobs.Job')),
                ('seeker', models.ForeignKey(to='accounts.JobSeeker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptionalJobSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job', models.ForeignKey(to='jobs.Job')),
                ('skill', models.ForeignKey(to='job_skills.JobSkill')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequiredJobSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job', models.ForeignKey(to='jobs.Job')),
                ('skill', models.ForeignKey(to='job_skills.JobSkill')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='jobmatch',
            unique_together=set([('job', 'seeker')]),
        ),
    ]
