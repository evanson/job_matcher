from django.conf.urls import patterns, url
import jobs

urlpatterns = patterns(
    '',
    url(r'^add_opening/$', 'jobs.views.add_job', name='add_job'),
    url(r'^my_job_openings/$', 'jobs.views.my_jobs', name='my_jobs'),
    url(r'^job_openings/(?P<id>\d+)/matches/$', 'jobs.views.job_matches', name='job_matches'),
    url(r'^my_job_matches/$', 'jobs.views.my_job_matches', name='my_job_matches'),
    url(r'^job_openings/(?P<id>\d+)/mark_interest/$', 'jobs.views.mark_interest_in_job', name='mark_interest'),
)
