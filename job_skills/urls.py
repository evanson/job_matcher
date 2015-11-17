from django.conf.urls import patterns, url
import job_skills

urlpatterns = patterns(
    '',
    url(r'^get_skills/$', 'job_skills.views.get_job_skills', name='get_job_skills'),
)
