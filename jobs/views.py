import logging
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import (login_required, permission_required,
                                            user_passes_test)
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings

from dashboard.views import server_error
from forms import JobForm
from models import Job, RequiredJobSkill, OptionalJobSkill
from accounts.models import Employer
from tasks import match_job


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
