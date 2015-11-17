from django.conf.urls import patterns, url
import accounts
from views import JobSeekerWizard, JOB_SEEKER_FORMS

jobseeker_wizard = JobSeekerWizard.as_view(JOB_SEEKER_FORMS, url_name='job_seeker_signup',
                                           done_step_name='done')

urlpatterns = patterns(
    '',
    url(r'^signup/jobseeker/(?P<step>.+)/$', jobseeker_wizard, name='job_seeker_signup'),
    url(r'^confirm/(?P<activation_key>\w+)/$', 'accounts.views.signup_confirm', name='email_confirm'),
    url(r'^logout/$', 'accounts.views.end_session', name='logout'),
    url(r'^profile/$', 'accounts.views.user_profile', name='profile'),
)
