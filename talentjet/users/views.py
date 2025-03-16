from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, ResumeUploadForm, ProfileUpdateForm
from .models import Profile
from jobs.models import Job  # Add this import
from applications.models import Application  # Add this import

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    context = {
        'profile': profile,
        'recent_applications': Application.objects.filter(applicant=request.user).order_by('-applied_at')[:5] if request.user.role == 'job_seeker' else None,
        'recent_jobs': Job.objects.filter(recruiter=request.user).order_by('-posted_at')[:5] if request.user.role == 'recruiter' else None,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_view(request):
    try:
        profile = request.user.profile
        if request.user.role == 'jobseeker':
            if request.method == 'POST' and 'resume_upload' in request.POST:
                resume_form = ResumeUploadForm(request.POST, request.FILES, instance=profile)
                if resume_form.is_valid():
                    resume_form.save()
                    messages.success(request, "Your resume has been uploaded successfully!")
                    return redirect('profile')
            else:
                resume_form = ResumeUploadForm(instance=profile)
        else:
            resume_form = None
        context = {
            'profile': profile,
            'resume_form': resume_form,
            # ...other context variables...
        }
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()
        resume_form = None
        context = {
            'profile': profile,
            'resume_form': resume_form,
            # ...other context variables...
        }
    return render(request, 'users/profile.html', context)

@login_required
def delete_resume(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.resume:
                profile.resume.delete()  # Delete the file
                profile.resume = None    # Clear the field
                profile.save()
                messages.success(request, "Your resume has been deleted successfully!")
            else:
                messages.warning(request, "No resume found to delete.")
        except Profile.DoesNotExist:
            messages.error(request, "Profile does not exist.")
    return redirect('profile')

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            user = request.user

            # Update user fields
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']

            # Update company information for recruiters
            if user.role == 'recruiter':
                user.company_name = form.cleaned_data['company_name']
                user.company_website = form.cleaned_data['company_website']
                user.company_description = form.cleaned_data['company_description']
                user.company_size = form.cleaned_data['company_size']
                user.company_industry = form.cleaned_data['company_industry']
                if form.cleaned_data.get('company_logo'):
                    user.company_logo = form.cleaned_data['company_logo']

            user.save()
            profile.save()

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile_update.html', {'form': form})

@login_required
def dashboard_view(request):
    """Display the appropriate dashboard based on user role."""
    user = request.user
    context = {}

    if user.role == 'job_seeker':
        # Job seeker dashboard data
        from jobs.models import Job
        from django.db.models import Q

        # Get user skills (assuming profile has a skills field or related model)
        user_skills = []
        if hasattr(user, 'profile') and user.profile:
            user_skills = [skill.lower() for skill in user.profile.skills.split(',') if skill.strip()]

        # Recent applications data
        context['applications'] = user.applications.all().select_related('job').order_by('-applied_at')[:5]
        context['applications_count'] = user.applications.count()

        # Recommended jobs based on skills
        recommended_jobs = []
        if user_skills:
            skill_filter = Q()
            for skill in user_skills:
                skill_filter |= Q(required_skills__icontains=skill)

            recommended_jobs = Job.objects.filter(
                skill_filter,
                is_active=True
            ).exclude(
                applications__applicant=user  # Exclude jobs user already applied to
            ).order_by('-posted_at')[:6]

        context['recommended_jobs'] = recommended_jobs

        # Profile completion percentage
        context['profile_completion'] = calculate_profile_completion(user)

        # Recent job activity
        context['recent_jobs'] = Job.objects.filter(is_active=True).order_by('-posted_at')[:3]

        template = 'users/seeker_dashboard.html'

    else:  # recruiter
        # Recruiter dashboard data
        from django.db.models import Count

        # Jobs statistics
        context['jobs'] = user.jobs.all()
        context['active_jobs_count'] = user.jobs.filter(is_active=True).count()
        context['total_jobs_count'] = user.jobs.count()

        # Applications statistics
        context['total_applications'] = sum(job.applications.count() for job in user.jobs.all())
        context['pending_applications'] = sum(job.applications.filter(status='pending').count() for job in user.jobs.all())
        context['accepted_applications'] = sum(job.applications.filter(status='accepted').count() for job in user.jobs.all())

        # Recent applications
        recent_applications = []
        for job in user.jobs.all():
            for app in job.applications.all().select_related('applicant')[:10]:
                recent_applications.append(app)
        recent_applications.sort(key=lambda x: x.applied_at, reverse=True)
        context['recent_applications'] = recent_applications[:5]

        # Top performing jobs
        context['top_jobs'] = user.jobs.annotate(
            app_count=Count('applications')
        ).order_by('-app_count')[:3]

        template = 'users/recruiter_dashboard.html'

    return render(request, template, context)

def calculate_profile_completion(user):
    """Calculate the profile completion percentage for a user."""
    # Base profile fields to check
    total_fields = 5  # Basic fields count
    completed_fields = 1  # Account exists = 1

    if hasattr(user, 'profile'):
        if user.profile.bio and len(user.profile.bio) > 10:
            completed_fields += 1
        if user.profile.skills:
            completed_fields += 1
        if user.profile.resume:
            completed_fields += 1
        if user.profile.phone_number:
            completed_fields += 1
        if user.profile.education:
            completed_fields += 1
            total_fields += 1

    return int((completed_fields / total_fields) * 100)
