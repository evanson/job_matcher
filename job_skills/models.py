from django.db import models


class JobSkill(models.Model):
    JOB_CATEGORIES = (('accounting', 'Accounting & Finance'), ('administration', 'Administration'), ('agriculture', 'Agriculture'),
                      ('architecture', 'Architecture'), ('audit', 'Auditing & Risk Management'),
                      ('banking', 'Banking & Investment'), ('business_administration', 'Business administration & management'),
                      ('communication', 'Communication & Public Relations'), ('community_development', 'Community Development & Social Work'),
                      ('customer_service', 'Customer Service'), ('design', 'Design'), ('education', 'Education & teaching'), ('engineering', 'Engineering'), 
                      ('health', 'Health & Medical Services'), ('hospitality', 'Hospitality'), ('IT', 'IT'), ('legal', 'Legal Services'),
                      ('media', 'Media & Journalism'), ('project_management', 'Project Management'), ('sales_marketing', 'Sales & Marketing'))

    category = models.SlugField(choices=JOB_CATEGORIES)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('category', 'name'),)
