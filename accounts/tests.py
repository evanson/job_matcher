from django.test import LiveServerTestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.core import mail


class TestJobSeekerSignup(LiveServerTestCase):
    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_signup(self):
        url = reverse('job_seeker_signup', kwargs={'step': 'user'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Job Seeker Sign Up')

        data = {'jobseeker_wizard-current_step': 'user', 'user-username': 'evanson',
                'user-first_name': 'Evanson', 'user-last_name': 'Wachira',
                'user-password1': 'evanson', 'user-password2': 'evanson',
                'user-email': 'evansonwachira@gmail.com',
                'user-country_code': '+254',
                'user-phone_number': '725911243',}
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Job Experience Details")

        profile_url = reverse('signup', kwargs={'step': 'job_seeker_profile'})
        profile_data = {'jobseeker_wizard-current_step': 'job_seeker_profile',
                        'category': 'IT', 'summary': 'Experienced software developer',
                        'years_of_experience': 4, 'skills': ['34', '35', '37',
                                                             '40', '44', '45',
                                                             '47', '50']}
        response = self.client.post(profile_url, data=profile_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response, "You've successfully signed up.")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Account Confirmation')
