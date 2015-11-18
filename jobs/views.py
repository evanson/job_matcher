import logging
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import (login_required, permission_required,
                                            user_passes_test)
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings

from job_matcher.settings import PER_PAGE
from dashboard.views import server_error
from forms import JobForm, InterestForm
from models import Job, RequiredJobSkill, OptionalJobSkill, JobMatch
from accounts.models import Employer, JobSeeker
from tasks import match_job
from decorators import can_view_matches_for_job, has_match_for_job


@login_required
@user_passes_test(lambda u: u.userprofile.role == 'employer')
def add_job(request):
    try:
        form = JobForm(request.POST or None)
        if form.is_valid():
            required_skills = set(form.cleaned_data['required_skills'])
            optional_skills = set(form.cleaned_data['optional_skills']) - required_skills
            with transaction.atomic():
                employer = Employer.objects.get(user=request.user)
                job = Job(employer=employer, description=form.cleaned_data['description'],
                          category=form.cleaned_data['category'],
                          years_of_experience=form.cleaned_data['years_of_experience'],
                          other=form.cleaned_data['other'])
                job.save()
                for skill in required_skills:
                    skill = RequiredJobSkill(job=job, skill=skill)
                    skill.save()
                if optional_skills:
                    for skill in optional_skills:
                        skill = OptionalJobSkill(job=job, skill=skill)
                        skill.save()
            match_job.delay(job.id)
            
            messages.success(request, "Job saved successfully. You'll receive matching candidates soon")
            return HttpResponseRedirect(reverse('profile'))
        return render(request, 'jobs/add_job.html', {'form': form})
    except Exception, e:
        logging.exception(e)
        return server_error(request)


@login_required
@user_passes_test(lambda u: u.userprofile.role == 'employer')
def my_jobs(request):
    try:
        employer = Employer.objects.get(user=request.user)
        jobs = Job.objects.filter(employer=employer).order_by('-created_at')
        page = request.GET.get('page')
        paginator = Paginator(jobs, PER_PAGE)
        try:
            pager = paginator.page(page)
        except PageNotAnInteger:
            pager = paginator.page(1)
        except EmptyPage:
            pager = paginator.page(paginator.num_pages)

        return render(request, 'jobs/my_jobs.html',
                      {'pager': pager})
    except Exception, e:
        logging.exception(e)
        return server_error(request)


@login_required
@can_view_matches_for_job
def job_matches(request, id):
    try:
        job = Job.objects.get(id=id)
        matches = JobMatch.objects.filter(job=job,
                                          status='interested').order_by(
                                              '-created_at', '-score')
        page = request.GET.get('page')
        paginator = Paginator(matches, PER_PAGE)
        try:
            pager = paginator.page(page)
        except PageNotAnInteger:
            pager = paginator.page(1)
        except EmptyPage:
            pager = paginator.page(paginator.num_pages)

        return render(request, 'jobs/job_matches.html',
                      {'pager': pager, 'job': job})
    except Exception, e:
        logging.exception(e)
        return server_error(request)


@login_required
@user_passes_test(lambda u: u.userprofile.role == 'job_seeker')
def my_job_matches(request):
    try:
        seeker = JobSeeker.objects.get(user=request.user)
        matches = JobMatch.objects.filter(seeker=seeker).order_by('-created_at', '-score')
        page = request.GET.get('page')
        paginator = Paginator(matches, PER_PAGE)
        try:
            pager = paginator.page(page)
        except PageNotAnInteger:
            pager = paginator.page(1)
        except EmptyPage:
            pager = paginator.page(paginator.num_pages)

        return render(request, 'jobs/my_job_matches.html',
                      {'pager': pager})
    except Exception, e:
        logging.exception(e)
        return server_error(request)


@login_required
@user_passes_test(lambda u: u.userprofile.role == 'job_seeker')
@has_match_for_job
def mark_interest_in_job(request, id):
    try:
        job = Job.objects.get(id=id)
        seeker = JobSeeker.objects.get(user=request.user)
        match = JobMatch.objects.get(job=job, seeker=seeker)
        form = InterestForm(request.POST or None)
        if form.is_valid():
            match.status = form.cleaned_data['status']
            match.save()

            messages.success(request,
                             'Your interest in the job has been marked as %s' % match.get_status_display())
            return HttpResponseRedirect('/')

        return render(request, 'jobs/mark_interest.html', {'job': job,
                                                           'form': form,
                                                           'match': match})
    except Exception, e:
        logging.exception(e)
        return server_error(request)
