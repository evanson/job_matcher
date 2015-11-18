import logging
import itertools
from django.core.mail import send_mail
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
                jobmatch = JobMatch(job=job, seeker=jobseeker, score=score,
                                    weight=weight)
                jobmatch.save()
    except Exception, e:
        logging.exception(e)
        return False
    return True
