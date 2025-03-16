# Django Framework: From Beginner to Building a Recruitment Portal

## 1. Introduction to Django

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It was designed by experienced developers to take care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

### Why Django?
- **Batteries included**: Django comes with many built-in features like authentication, admin panel, and ORM
- **Security**: Helps developers avoid common security mistakes
- **Scalable**: Powers sites like Instagram and Pinterest
- **Versatile**: Works well for almost any type of website

## 2. Setting Up Your Environment

### Installing Python and Django
```bash
# Install Python (if not already installed)
# Download from python.org or use package manager

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Django
pip install django

# Verify installation
python -m django --version
```

### Creating Your First Project
```bash
# Create a new Django project
django-admin startproject recruitmentmanagement

# Navigate to the project directory
cd recruitmentmanagement

# Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to see the default Django welcome page.

## 3. Understanding Project Structure

After creating your project, Django generates the following structure:

```
recruitmentmanagement/
    manage.py                 # Command-line utility to interact with your project
    recruitmentmanagement/    # Project package
        __init__.py           # Empty file that tells Python this is a package
        settings.py           # Project settings/configuration
        urls.py               # URL declarations for the project
        asgi.py               # Entry point for ASGI web servers (like Daphne)
        wsgi.py               # Entry point for WSGI web servers (like Gunicorn)
```

### Key Files to Understand:
- **manage.py**: Command-line utility to perform various Django commands
- **settings.py**: Configuration of your Django project
- **urls.py**: URL configuration (like a table of contents for your website)

## 4. Creating Django Apps

In Django, a project is made up of one or more "apps," which are modular components focused on specific functionality.

```bash
# Create an app for user management
python manage.py startapp users

# Create an app for job listings
python manage.py startapp jobs

# Create an app for job applications
python manage.py startapp applications
```

Register your apps in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    'users.apps.UsersConfig',
    'jobs.apps.JobsConfig',
    'applications.apps.ApplicationsConfig',
]
```

## 5. Models and Database Design

Models in Django are Python classes that define the structure of your database tables.

### Example Models for a Recruitment System:

```python
# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seeker')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    skills = models.JSONField(default=list, blank=True, null=True)

    # Recruiter specific fields
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
```

```python
# jobs/models.py
from django.db import models
from users.models import User

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    )

    title = models.CharField(max_length=255)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    required_skills = models.JSONField(default=list)
```

### Migrations
After defining models, you need to create migrations and apply them to your database:

```bash
# Generate migration files based on models
python manage.py makemigrations

# Apply migrations to the database
python manage.py migrate
```

## 6. Django Admin Interface

One of Django's most powerful features is its automatic admin interface.

```python
# users/admin.py
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'first_name', 'last_name']
    list_filter = ['role', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'company_name']
```

Create a superuser to access the admin:
```bash
python manage.py createsuperuser
```

## 7. URLs and Views

### URL Configuration

URLs map web addresses to views.

```python
# recruitmentmanagement/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # For main site pages
    path('users/', include('users.urls')),
    path('jobs/', include('jobs.urls')),
]
```

```python
# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/update/', views.job_update, name='job_update'),
    path('search/', views.job_search, name='job_search'),
]
```

### Views

Views handle HTTP requests and return HTTP responses. They're the interface between models/templates and the user.

```python
# jobs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def job_create(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user
            job.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form})
```

## 8. Templates and Frontend

Django uses a template system for the frontend. Templates are HTML files with Django template language added.

### Directory Structure
```
templates/
    base.html                # Main template other templates extend
    home.html                # Homepage
    jobs/
        job_list.html        # List of jobs
        job_detail.html      # Single job detail
        job_form.html        # Create/update job form
    users/
        login.html           # Login page
        signup.html          # Registration page
        dashboard.html       # User dashboard
        profile.html         # User profile
```

### Example Base Template
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TalentJet{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">TalentJet</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'job_list' %}">Browse Jobs</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'dashboard' %}">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'profile' %}">Profile</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'login' %}">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'signup' %}">Sign Up</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Content -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <p class="text-center mb-0">© {% now "Y" %} TalentJet. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Example Job List Template
```html
<!-- templates/jobs/job_list.html -->
{% extends 'base.html' %}

{% block title %}Browse Jobs | TalentJet{% endblock %}

{% block content %}
<div class="container my-5">
    <h1 class="mb-4">Find Your Dream Job</h1>

    <div class="row">
        <!-- Filters -->
        <div class="col-md-3 mb-4">
            <div class="card shadow-sm">
                <div class="card-header bg-white py-3">
                    <h4 class="card-title mb-0">Filters</h4>
                </div>
                <div class="card-body">
                    <form method="get">
                        <!-- Filter form elements -->
                        <div class="mb-3">
                            <label class="form-label">Job Type</label>
                            <!-- Filter checkboxes -->
                        </div>

                        <button type="submit" class="btn btn-primary w-100">Apply Filters</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Job listings -->
        <div class="col-md-9">
            {% if jobs %}
                <div class="job-listings">
                    {% for job in jobs %}
                        <div class="card shadow-sm mb-4">
                            <div class="card-body">
                                <div class="d-flex justify-content-between">
                                    <div>
                                        <h3 class="card-title">{{ job.title }}</h3>
                                        <p class="text-muted mb-2">{{ job.company.company_name }}</p>
                                    </div>
                                    <div>
                                        <span class="badge bg-secondary">{{ job.job_type }}</span>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <span class="me-3"><i class="fas fa-map-marker-alt"></i> {{ job.location }}</span>
                                    {% if job.salary_range %}
                                        <span><i class="fas fa-money-bill"></i> {{ job.salary_range }}</span>
                                    {% endif %}
                                </div>

                                <p class="card-text">{{ job.description|truncatewords:30 }}</p>

                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <span class="text-muted">Posted {{ job.created_at|timesince }} ago</span>
                                    </div>
                                    <a href="{% url 'job_detail' job.id %}" class="btn btn-outline-primary">View Details</a>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="text-center py-5">
                    <h3>No jobs found</h3>
                    <p>Try adjusting your search criteria.</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

## 9. Forms and User Input

Django forms make it easy to handle user input, validation, and CSRF protection.

### Creating Forms

```python
# jobs/forms.py
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'location', 'description', 'requirements', 'salary_range',
                 'job_type', 'required_skills']
        widgets = {
            'required_skills': forms.TextInput(attrs={'placeholder': 'Enter skills separated by commas'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_required_skills(self):
        skills = self.cleaned_data.get('required_skills')
        if isinstance(skills, str):
            # Convert comma-separated string to list
            return [skill.strip() for skill in skills.split(',') if skill.strip()]
        return skills
```

```python
# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
```

### Using Forms in Templates

```html
<!-- templates/jobs/job_form.html -->
{% extends 'base.html' %}

{% block title %}{{ form.instance.id|yesno:"Edit,Create" }} Job | TalentJet{% endblock %}

{% block content %}
<div class="container my-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm">
                <div class="card-header bg-white py-3">
                    <h4 class="card-title mb-0">{{ form.instance.id|yesno:"Edit Job,Post a New Job" }}</h4>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}

                        {% for field in form %}
                            <div class="mb-3">
                                <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                                {{ field }}
                                {% if field.help_text %}
                                    <small class="form-text text-muted">{{ field.help_text }}</small>
                                {% endif %}
                                {% if field.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ field.errors }}
                                    </div>
                                {% endif %}
                            </div>
                        {% endfor %}

                        <div class="text-end">
                            <button type="submit" class="btn btn-primary">{{ form.instance.id|yesno:"Update,Post" }} Job</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 10. Authentication and User Management

Django comes with a built-in authentication system that you can extend.

### Custom Authentication Views

```python
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or 'dashboard'
                return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})
```

### Login Required Decorator

Use `@login_required` to restrict access to logged-in users:

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # ... view code that requires login
```

## 11. Adding Dashboard for Different User Types

```python
# users/views.py
@login_required
def dashboard(request):
    """Display the appropriate dashboard based on user role."""
    user = request.user

    if user.role == 'seeker':
        # Job seeker specific context data
        applications = user.applications.all().select_related('job')
        context = {
            'applications': applications,
            'recommended_jobs': get_recommended_jobs(user),
        }
        return render(request, 'users/seeker_dashboard.html', context)
    else:  # recruiter
        # Recruiter specific context data
        jobs = user.jobs.all()
        applications = [app for job in jobs for app in job.applications.all()]
        context = {
            'jobs': jobs,
            'applications': applications,
        }
        return render(request, 'users/recruiter_dashboard.html', context)
```

## 12. Search Functionality

```python
# jobs/views.py
from django.db.models import Q

def job_search(request):
    query = request.GET.get('q', '')
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')

    jobs = Job.objects.filter(is_active=True)

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(requirements__icontains=query) |
            Q(required_skills__contains=[query])
        )

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, 'jobs/job_search.html', {
        'jobs': jobs,
        'query': query,
        'job_type': job_type,
        'location': location,
    })
```

## 13. Job Application System

```python
# applications/models.py
from django.db import models
from users.models import User
from jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('interviewing', 'Interviewing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'applicant')  # Each user can apply to a job once

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
```

```python
# applications/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm
from jobs.models import Job

@login_required
def apply_job(request, job_id):
    if request.user.role != 'seeker':
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('job_detail', pk=job_id)

    job = get_object_or_404(Job, pk=job_id, is_active=True)

    # Check if already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect('job_detail', pk=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply.html', {
        'form': form,
        'job': job
    })
```

## 14. Static Files and Media Files

### Settings Configuration

```python
# settings.py
# ... other settings ...

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### URL Configuration for Media Files

```python
# urls.py (main project urls.py)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your other url patterns ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 15. Advanced Topics

### Custom User Model

Setting up a custom user model is a best practice in Django, but must be done at the start of the project.

```python
# settings.py
AUTH_USER_MODEL = 'users.User'
```

### Signals

Signals allow certain events to trigger actions.

```python
# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a profile for each new user."""
    if created:
        Profile.objects.create(user=instance)
```

### Middleware

Middleware processes requests and responses globally. For example, a middleware to track page views:

```python
# analytics/middleware.py
from .models import PageView

class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only log successful page views
        if response.status_code == 200 and not request.path.startswith('/admin/'):
            PageView.objects.create(
                path=request.path,
                user=request.user if request.user.is_authenticated else None
            )

        return response
```

### Custom Template Tags

Create custom template tags for complex logic:

```python
# jobs/templatetags/job_tags.py
from django import template
from django.db.models import Count
from jobs.models import Job

register = template.Library()

@register.simple_tag
def get_top_companies(count=5):
    """Get companies with the most job postings."""
    return Job.objects.values('company__company_name', 'company__id') \
                      .annotate(job_count=Count('id')) \
                      .order_by('-job_count')[:count]
```

## 16. Deployment

When deploying your Django project, consider these steps:

1. Set `DEBUG = False` in production
2. Configure proper database (e.g., PostgreSQL)
3. Set secure `SECRET_KEY`
4. Configure HTTPS
5. Run `python manage.py collectstatic` to collect static files
6. Use a production WSGI server like Gunicorn
7. Consider using Docker and a service like Heroku, AWS, or DigitalOcean

## 17. Testing Your Application

Django provides a testing framework:

```python
# jobs/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Job
from users.models import User

class JobModelTests(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create(username='recruiter', role='recruiter')
        self.job = Job.objects.create(
            title='Django Developer',
            company=self.recruiter,
            location='Remote',
            description='Build web applications using Django',
            requirements='Python, Django knowledge',
            job_type='full_time'
        )

    def test_job_creation(self):
        self.assertEqual(self.job.title, 'Django Developer')
        self.assertEqual(self.job.is_active, True)

class JobViewTests(TestCase):
    def setUp(self):
        # Create test data
        pass

    def test_job_list_view(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_list.html')
```

## Next Steps

Now that you have a foundational understanding of Django, here are some advanced topics to explore:

1. **Django REST framework** - For building APIs
2. **Caching** - To improve performance
3. **Celery** - For handling background tasks
4. **Django Channels** - For real-time features like chat
5. **Elasticsearch** - For advanced search capabilities

## Resources for Further Learning

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Mozilla Developer Network (MDN) Django Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)
- [Test-Driven Development with Django](https://testdriven.io/)

Good luck with your Django journey! Building a recruitment management system will give you great experience with many aspects of web development.
