from django.db import models
from django.utils import timezone
from users.models import CustomUser

class Job(models.Model):
    JOB_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
    )

    EXPERIENCE_LEVELS = (
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
    )

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default='entry')
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    salary = models.CharField(max_length=100, blank=True, help_text="E.g., $50K-$70K or Competitive")
    posted_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posted_jobs')
    required_skills = models.CharField(max_length=255)

    @property
    def display_date(self):
        return self.posted_at

    def __str__(self):
        return self.title
