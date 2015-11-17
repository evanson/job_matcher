import itertools
import json
from django.http import HttpResponse
from models import JobSkill


def get_job_skills(request):
    try:
        skills = {}
        category = request.GET.get('category')
        category_skills = JobSkill.objects.filter(category=category.strip()).order_by('name')
        for skill in category_skills:
            skills[skill.id] = skill.name
    except Exception, e:
        skills = {}
    return HttpResponse(json.dumps(skills), content_type='application/json')
