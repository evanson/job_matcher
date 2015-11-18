from django.db import models

from job_skills.models import JobSkill
from accounts.models import JobSeeker, Employer


class Job(models.Model):
    employer = models.ForeignKey(Employer)
    description = models.CharField(max_length=600,
                                   verbose_name="Description of the responsibilities for the job")
    category = models.SlugField(choices=JobSkill.JOB_CATEGORIES)
    years_of_experience = models.IntegerField(verbose_name="Minimum years of experience required")
    other = models.CharField(max_length=600, verbose_name="Additional Information")
    created_at = models.DateTimeField(auto_now_add=True)

    def jobmatches(self):
        return self.jobmatch_set.filter(status='interested').count()


class RequiredJobSkill(models.Model):
    job = models.ForeignKey(Job)
    skill = models.ForeignKey(JobSkill)


class OptionalJobSkill(models.Model):
    job = models.ForeignKey(Job)
    skill = models.ForeignKey(JobSkill)


class JobMatch(models.Model):
    WEIGHT_CHOICES = (('strong', 'Strong Match'),
                      ('exact', 'Exact Match'),
                      ('weak', 'Weak Match'))

    STATUS_CHOICES = (('interested', 'Interested'),
                      ('not_interested', 'Not Interested'))
    
    job = models.ForeignKey(Job)
    seeker = models.ForeignKey(JobSeeker)
    score = models.FloatField(default=0.0)
    weight = models.SlugField(choices=WEIGHT_CHOICES)
    notification_sent = models.BooleanField(default=False)
    status = models.SlugField(choices=STATUS_CHOICES, default='interested')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('job', 'seeker'),)   # Only one match per job per job seeker
