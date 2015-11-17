from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from job_skills.models import JobSkill


class UserProfile(models.Model):
    ROLE_CHOICES = (('admin', 'Admin'),
                    ('job_seeker', 'Job Seeker'),
                    ('employer', 'Employer')
    )
    user = models.OneToOneField(User)
    role = models.SlugField(choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, null=True, blank=True)
    activation_key = models.CharField(max_length=40, blank=True, null=True)
    key_expires = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class JobSeeker(models.Model):
    
    user = models.OneToOneField(User)
    category = models.SlugField(choices=JobSkill.JOB_CATEGORIES)
    summary = models.CharField(max_length=500,
                               verbose_name="A brief summary of who you are & your capabilities")
    years_of_experience = models.IntegerField()


class JobSeekerSkill(models.Model):
    seeker = models.ForeignKey(JobSeeker)
    skill = models.ForeignKey(JobSkill)


class Employer(models.Model):
    user = models.OneToOneField(User)
    company = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=60)
    address = models.CharField(max_length=50)
