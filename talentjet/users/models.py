from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    company = models.CharField(max_length=100, blank=True, null=True)  # Company for recruiters
    experience = models.TextField(blank=True, null=True)  # Experience for job seekers
    company_name = models.CharField(max_length=255, blank=True)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    company_industry = models.CharField(max_length=100, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True,
        blank=True,
        help_text="Upload your resume in PDF, DOC, or DOCX format (Max size: 5MB)"
    )
