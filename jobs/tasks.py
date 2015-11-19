import logging
import itertools
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.db import IntegrityError
from django.conf import settings
from job_matcher import app

from matcher import matcher
from models import Job, JobMatch
from accounts.models import JobSeeker, JobSeekerSkill


@app.task
def match_job(jobID):
    try:
        job = Job.objects.get(id=jobID)
        required_skills = list(itertools.chain(*job.requiredjobskill_set.values_list('skill__name')))
        optional_skills = list(itertools.chain(*job.optionaljobskill_set.values_list('skill__name')))
        requirements = {'years': int(job.years_of_experience),
                        'skills': required_skills,
                        'optional': optional_skills}
        
        candidates = JobSeeker.objects.filter(category=job.category)
        for jobseeker in candidates:
            skills = list(itertools.chain(*JobSeekerSkill.objects.filter(
                seeker=jobseeker).values_list('skill__name')))
            candidate = {'name': jobseeker.user.get_full_name(), 'skills': skills,
                         'years': int(jobseeker.years_of_experience)}

            matched, score, weight = matcher(requirements, candidate)
            if matched:
                try:
                    jobmatch = JobMatch(job=job, seeker=jobseeker, score=score,
                                        weight=weight)
                    jobmatch.save()
                except IntegrityError, e:   # Match already exists
                    logging.exception(e)
                    pass

    except Exception, e:
        logging.exception(e)
        return False
    return True


@app.task
def match_candidate(jobseekerID):
    try:
        jobseeker = JobSeeker.objects.get(id=jobseekerID)
        skills = list(itertools.chain(*jobseeker.jobseekerskill_set.all().values_list('skill__name')))
        candidate = {'name': jobseeker.user.get_full_name(), 'skills': skills,
                     'years': int(jobseeker.years_of_experience)}
        
        # For new candidates, do a match for jobs added in the last 30 days only
        date = timezone.now() - timedelta(days=30)
        jobs = Job.objects.filter(category=jobseeker.category, created_at__gte=date)
        for job in jobs:
            required_skills = list(itertools.chain(
                *job.requiredjobskill_set.values_list('skill__name')))

            optional_skills = list(itertools.chain(
                *job.optionaljobskill_set.values_list('skill__name')))

            requirements = {'years': int(job.years_of_experience),
                            'skills': required_skills,
                            'optional': optional_skills}
            matched, score, weight = matcher(requirements, candidate)
            if matched:
                try:
                    jobmatch = JobMatch(job=job, seeker=jobseeker, score=score,
                                        weight=weight)
                    jobmatch.save()
                except IntegrityError, e:   # Match already exists
                    logging.exception(e)
                    pass
    except Exception, e:
        logging.exception(e)
        return False
    return True
