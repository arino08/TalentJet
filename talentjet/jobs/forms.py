from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'description', 'location', 'job_type',
                 'experience_level', 'required_skills', 'salary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Senior Software Developer'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your company name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Describe the job responsibilities, qualifications, and benefits'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., New York or Remote'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_level': forms.Select(attrs={'class': 'form-control'}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Python, Django, JavaScript'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., $50K-$70K or Competitive'}),
        }
