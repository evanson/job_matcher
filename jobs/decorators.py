from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist

from models import Job


def can_view_matches_for_job(func, *args, **kwargs):
    def wrapper(request, *args2, **kwargs2):
        try:
            user = request.user
            if user.is_staff:
                return func(request, *args2, **kwargs2)
            else:
                jobid = kwargs2['id']
                job = Job.objects.get(id=jobid)
                if job.employer.user == user:
                    return func(request, *args2, **kwargs2)

            messages.error(request, 'Access Denied')
            return HttpResponseRedirect('/')
            
        except ObjectDoesNotExist:
            raise Http404('Sorry, couldn\'t get the page you were looking for')

    return wrapper
