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
