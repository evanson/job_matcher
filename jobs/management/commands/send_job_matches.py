import itertools
from django.template.loader import get_template
from django.template import Context
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings

from accounts.models import JobSeeker
from jobs.models import JobMatch

class Command(BaseCommand):
    help = '''Send matching jobs to job seekers daily'''

    def handle(self, *args, **options):
        unnotified_job_seekers = set(list(itertools.chain(
            *JobMatch.objects.filter(notification_sent=False).values_list('seeker'))))

        for jobseeker in unnotified_job_seekers:
            jobmatches = JobMatch.objects.filter(notification_sent=False, seeker=jobseeker)
            user = JobSeeker.objects.get(id=jobseeker).user

            ctx = {'user': user, 'matches': jobmatches}

            subject = 'New Job Matches'

            message = get_template('jobs/emails/job_seeker_job_matches.html').render(Context(ctx))
            msg = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user.email])
            msg.content_subtype = 'html'
            print "Sending job matches to %s" % user.get_full_name()
            msg.send()

            for match in jobmatches:
                match.notification_sent = True
                match.save()
