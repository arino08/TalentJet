from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    company = forms.CharField(max_length=100, required=False)
    experience = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'company', 'experience')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.company = self.cleaned_data['company']
        user.experience = self.cleaned_data['experience']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'company', 'experience')

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['resume']
        widgets = {
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size (limit to 5MB)
            if resume.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise forms.ValidationError("File size must be under 5MB.")

            # Check file extension
            allowed_extensions = ['pdf', 'doc', 'docx']
            ext = resume.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(f"Only {', '.join(allowed_extensions)} files are allowed.")

        return resume

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    company_name = forms.CharField(max_length=100, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    location = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=15, required=False)
    skills = forms.CharField(widget=forms.Textarea, required=False,
                           help_text="Enter your skills (comma separated)")
    resume = forms.FileField(required=False)

    # Company fields
    company_name = forms.CharField(max_length=255, required=False)
    company_website = forms.URLField(required=False)
    company_description = forms.CharField(widget=forms.Textarea, required=False)
    company_size = forms.CharField(max_length=50, required=False)
    company_industry = forms.CharField(max_length=100, required=False)
    company_logo = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'phone', 'resume', 'skills']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['company_name'].initial = self.instance.user.company_name if hasattr(self.instance.user, 'company_name') else ''
            user = self.instance.user
            self.fields['company_name'].initial = user.company_name
            self.fields['company_website'].initial = user.company_website
            self.fields['company_description'].initial = user.company_description
            self.fields['company_size'].initial = user.company_size
            self.fields['company_industry'].initial = user.company_industry

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        # Update user's company information
        if user.role == 'recruiter':
            user.company_name = self.cleaned_data['company_name']
            user.company_website = self.cleaned_data['company_website']
            user.company_description = self.cleaned_data['company_description']
            user.company_size = self.cleaned_data['company_size']
            user.company_industry = self.cleaned_data['company_industry']
            if self.cleaned_data.get('company_logo'):
                user.company_logo = self.cleaned_data['company_logo']
            user.save()

        if commit:
            profile.save()
        return profile
