from django import forms
from job_skills.models import JobSkill


class JobForm(forms.Form):
    category = forms.ChoiceField(choices=JobSkill.JOB_CATEGORIES)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': '20',
                                                                'rows': '20'}))
    years_of_experience = forms.IntegerField(label='Minimum years of experience')
    required_skills = forms.ModelMultipleChoiceField(queryset=JobSkill.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple())
    optional_skills = forms.ModelMultipleChoiceField(queryset=JobSkill.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple(),
                                                      required=False)
    other = forms.CharField(widget=forms.Textarea(attrs={'cols': '20',
                                                          'rows': '15'}),
                             label='Any other Job requirements')
