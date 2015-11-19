from django.test import LiveServerTestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.core import mail

from django.core.exceptions import ObjectDoesNotExist
from job_skills.models import JobSkill


class TestJobSeekerSignup(LiveServerTestCase):
    def setUp(self):
        skills = {'accounting': ['Book Keeping', 'Balance Sheets', 'P & L', 'Petty Cash Management', 'Taxation',  'Cost Management', 'Budgeting'],
                  
                  'administration': ['Data Entry', 'Virtual Assistance', 'Research', 'Transcription', 'Secretarial'],
                  
                  'agriculture': ['Vertinary', 'Crop Production', 'Large Scale Farming', 'Animal Husbandry'],
                  
                  'audit': ['Auditing', 'Risk Analysis', ],
                  
                  'banking': ['Customer Acquisition', 'Credit Management', 'Corporate Banking'],
                  
                  'business_administration': ['Business Plans', 'Corporate Governance'],
                  
                  'communication': ['Public Relations', 'Media Relations'],
                  
                  'community_development': ['Humanitarian work'],
                  
                  'customer_service': ['Call center management', 'Customer Relationship Management'],
                  
                  'design': ['Logos', 'Graphic Design', 'Illustration', 'Brochures', 'Banner Ads', 'Videos', 'Corporate Identity', 'Adobe Illustrator', 'Adobe Photoshop',
                             '3D Modelling', '3D Animation', '2D Animation', '2D Modelling'],
                  
                  'education': ['ECD'],
                  
                  'engineering': ['CAD', 'Electrical', 'Architecture', 'Mechanical', 'Product Design', 'Civil', 'Structural', 'Contract Manufacturing'],
                  
                  'health': ['General Practitioning', 'Nursing', 'Public Health'],
                  
                  'hospitality': ['Restaurant Management', 'Outside Catering', 'Tourism Operations'],
                  

                  'IT': ['ASP.NET', 'C#', 'MySQL', 'Postgres', 'MsSQL', 'C#', 'VB.NET', 'C', 'C++', 'Windows Administration', 'Linux Administration', 'iOS development',
                         'Windows Phone Development', 'Android Development', 'Python', 'Ruby', 'Java', 'Javascript', 'Node JS', 'Angular JS', 'Ruby on Rails', 'Django',
                         'Oracle', 'PHP', 'CSS', 'HTML', 'Networking & Security', 'CCNA', 'WordPress', 'Shopify', 'Joomla', 'Erlang', 'Golang', 'Delphi', 'Clojure',
                         'Scala', 'Haskell', 'Adobe Acrobat', 'MongoDB', 'Cassandra', 'CouchDB', 'Riak', 'Perl', 'Ocaml', 'Lisp', 'Rust', 'VOIP', 'Web Scraping', 'Laravel',
                         'Zend Framework', 'CodeIgniter', 'CakePHP', 'Symfony'],
                  
                  'legal': ['Contracts', 'Intellectual Property', 'Corporate', 'Real Estate', 'Wills, Trusts, Estates', 'Bankruptcy', 'Criminal Defence'],
                  
                  'media': ['TV Production', 'Radio Production', 'Video Production', 'Video Editing', 'Publishing', 'Editorial' ],
                  
                  'project_management': ['Cost Estimation', 'Scheduling', 'Staffing'],
                  
                  'sales_marketing': ['Ad campaigns', 'B2B Marketing', 'Corporate Sales', 'Email Marketing', 'Lead Generation', 'Marketing Strategy', 'Search Engine Marketing',
                              'Telemarketing']}

        for category, category_skills in skills.iteritems():
            for skill in category_skills:
                try:
                    s = JobSkill.objects.get(category=category, name=skill)
                except ObjectDoesNotExist:
                    s = JobSkill(category=category, name=skill)
                    s.save()

        
    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_signup(self):
        url = reverse('job_seeker_signup', kwargs={'step': 'user'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')

        data = {'job_seeker_wizard-current_step': 'user', 'user-username': 'evanson',
                'user-first_name': 'Evanson', 'user-last_name': 'Wachira',
                'user-password1': 'evanson', 'user-password2': 'evanson',
                'user-email': 'evansonwachira@gmail.com',
                'user-country_code': '+254',
                'user-phone_number': '725911243',}
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Job Experience Details")

        profile_url = reverse('job_seeker_signup', kwargs={'step': 'job_seeker_profile'})
        profile_data = {'job_seeker_wizard-current_step': 'job_seeker_profile',
                        'job_seeker_profile-category': 'IT',
                        'job_seeker_profile-summary': 'Experienced software developer',
                        'job_seeker_profile-years_of_experience': 4,
                        'job_seeker_profile-skills': ['34', '35', '37',
                                   '40', '44', '45',
                                   '47', '50']}
        response = self.client.post(profile_url, data=profile_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You've successfully signed up.")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Account Confirmation')

        activation_link = mail.outbox[0].body.split('link ')[1]
        print activation_link
