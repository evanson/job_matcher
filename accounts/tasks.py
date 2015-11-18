import logging
from django.core.mail import send_mail
from django.conf import settings
from job_matcher import app
from job_matcher import twilio_client

@app.task
def send_email(subject, message, recipients):
    try:
        logging.info("Sending message '{}' to {}".format(message, recipients))
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipients,
                  fail_silently=False)
    except Exception, e:
        logging.exception(e)
        return False
    return True
