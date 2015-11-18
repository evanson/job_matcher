from django.conf.urls import patterns, url
import jobs

urlpatterns = patterns(
    '',
    url(r'^add_opening/$', 'jobs.views.add_job', name='add_job'),
)
