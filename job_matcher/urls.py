from django.conf.urls import patterns, include, url
from django.contrib import admin

import dashboard
import accounts
import job_skills


urlpatterns = patterns(
    '',
    url(r'^$', 'dashboard.views.index', name='index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^jobs/categories/', include('job_skills.urls'))
)
