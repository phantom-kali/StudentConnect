from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'salary', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.job = kwargs.pop('job', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if Application.objects.filter(job=self.job, applicant=self.user).exists():
            raise forms.ValidationError("You have already applied for this job.")
        return cleaned_data

class JobFilterForm(forms.Form):
    title = forms.CharField(required=False)
    company = forms.CharField(required=False)
    location = forms.CharField(required=False)
    status = forms.ChoiceField(choices=[('', 'All')] + Job.STATUS_CHOICES, required=False)
    sort_by = forms.ChoiceField(choices=[
        ('created_at', 'Newest'),
        ('-created_at', 'Oldest'),
        ('title', 'Title (A-Z)'),
        ('-title', 'Title (Z-A)'),
    ], required=False)
