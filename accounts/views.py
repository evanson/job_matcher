import logging
import re
import random
import hashlib
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings

from dashboard.views import server_error
from models import UserProfile, JobSeeker, JobSeekerSkill, Employer
from forms import CreateUserForm, JobSeekerForm, EmployerForm

from tasks import send_email


def end_session(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url=reverse_lazy('login', kwargs={'step': 'user'}))
def user_profile(request):
    try:
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        return render(request, 'accounts/profile.html', {'user': user,
                                                         'user_profile': user_profile})
    except Exception, e:
        logging.exception(e)
        return server_error(request)


JOB_SEEKER_FORMS = (
    ('user', CreateUserForm),
    ('job_seeker_profile', JobSeekerForm)
)

JOB_SEEKER_TEMPLATES = {
    'user': 'accounts/user.html',
    'job_seeker_profile': 'accounts/job_seeker_profile.html',
}


class JobSeekerWizard(NamedUrlSessionWizardView):
    def __init__(self, *args, **kwargs):
        super(JobSeekerWizard, self).__init__(*args, **kwargs)
        self.initial_dict = {"user": {"country_code": "+254"}}

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('profile'))
        return super(JobSeekerWizard, self).dispatch(*args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(JobSeekerWizard, self).get_context_data(form=form, **kwargs)
        context.update({'user_title': 'Job Seeker'})

        return context

    def get_template_names(self):
        return [JOB_SEEKER_TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        with transaction.atomic():
            user_data = form_dict['user'].cleaned_data
            phone_number = user_data['country_code'] + user_data['phone_number']
            email = user_data['email']
            username = user_data['username']

            user = form_dict['user'].save()

            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = timezone.now() + timedelta(days=30)

            user_profile = UserProfile(user=user, phone=phone_number,
                                       role='job_seeker',
                                       activation_key=activation_key,
                                       key_expires=key_expires)
            user_profile.save()

            email_subject = 'Account Confirmation'
            confirmation_url = self.request.build_absolute_uri(reverse('email_confirm',
                                                                       kwargs={'activation_key': activation_key}))
            email_body = "Hello %s, thanks for signing up. To activate your account,\
click this link %s" % (username, confirmation_url)

            send_email.delay(email_subject, email_body, [email])

            seeker_data = form_dict['job_seeker_profile'].cleaned_data

            jobseekerprofile = JobSeeker(user=user, category=seeker_data['category'],
                                         summary=seeker_data['summary'],
                                         years_of_experience=seeker_data['years_of_experience'])
            jobseekerprofile.save()

            for skill in seeker_data['skills']:
                jobskill = JobSeekerSkill(seeker=jobseekerprofile, skill=skill)
                jobskill.save()
            
            messages.success(self.request,
                             "You've successfully signed up. Please click the activation link sent to your email to activate your account")
            return HttpResponseRedirect('/')


COMPANY_FORMS = (
    ('user', CreateUserForm),
    ('company_profile', EmployerForm)
)

COMPANY_TEMPLATES = {
    'user': 'accounts/user.html',
    'company_profile': 'accounts/company_profile.html',
}


class CompanyWizard(NamedUrlSessionWizardView):
    def __init__(self, *args, **kwargs):
        super(CompanyWizard, self).__init__(*args, **kwargs)
        self.initial_dict = {"user": {"country_code": "+254"}}

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('profile'))
        return super(CompanyWizard, self).dispatch(*args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(CompanyWizard, self).get_context_data(form=form, **kwargs)
        context.update({'user_title': 'Company'})

        return context

    def get_template_names(self):
        return [COMPANY_TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        with transaction.atomic():
            user_data = form_dict['user'].cleaned_data
            phone_number = user_data['country_code'] + user_data['phone_number']
            email = user_data['email']
            username = user_data['username']

            user = form_dict['user'].save()
                
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = timezone.now() + timedelta(days=30)

            user_profile = UserProfile(user=user, phone=phone_number,
                                       role='employer',
                                       activation_key=activation_key,
                                       key_expires=key_expires)
            user_profile.save()

            email_subject = 'Account Confirmation'
            confirmation_url = self.request.build_absolute_uri(reverse('email_confirm',
                                                                      kwargs={'activation_key': activation_key}))
            email_body = "Hello %s, thanks for signing up. To activate your account,\
click this link %s" % (username, confirmation_url)
            send_email.delay(email_subject, email_body, [email])

            profile_data = form_dict['company_profile'].cleaned_data
            employer = Employer(user=user, company=profile_data['company_name'],
                                description=profile_data['description'],
                                location=profile_data['location'],
                                address=profile_data['address'])
            employer.save()

        messages.success(self.request,
                         "You've successfully signed up. Please click the activation link sent to your email to activate your account")
        return HttpResponseRedirect('/')


def signup_confirm(request, activation_key):
    try:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
        if user_profile.key_expires < timezone.now():
            messages.error(request, "Your account confirmation period has expired")
            return HttpResponseRedirect('/')
        user = user_profile.user
        user.is_active = True
        user.save()
        messages.success(request, "You've successfully activated your account")
        return HttpResponseRedirect('/')
    except ObjectDoesNotExist:
        return Http404()
    except Exception, e:
        logging.exception(e)
        return server_error(request)
