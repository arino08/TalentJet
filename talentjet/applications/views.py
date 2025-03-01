from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch
from .models import Application
from jobs.models import Job
from users.models import Profile

@login_required
def apply_for_job(request, job_id):
    if request.user.role != 'job_seeker':
        return redirect('job_list')

    job = get_object_or_404(Job, id=job_id)

    # Check if user already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        return redirect('job_detail', pk=job.pk)

    # Create application
    application = Application(job=job, applicant=request.user)
    application.save()

    return redirect('my_applications')

@login_required
def my_applications(request):
    # Only allow job seekers to access this page
    if request.user.role != 'job_seeker':
        messages.error(request, "You don't have permission to view this page.")
        return redirect('home')

    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job').order_by('-applied_at')

    context = {
        'applications': applications
    }
    return render(request, 'applications/my_applications.html', context)

@login_required
def manage_applications(request):
    # Only allow recruiters to access this page
    if request.user.role != 'recruiter':
        messages.error(request, "You don't have permission to view this page.")
        return redirect('home')

    # Use select_related and prefetch_related for optimal performance
    # This loads all related objects in a single query
    applications = Application.objects.filter(
        job__recruiter=request.user
    ).select_related(
        'job',
        'applicant',
        'applicant__profile'
    ).order_by('-applied_at')

    # Prefetch resumes here to avoid N+1 queries
    applications = applications.prefetch_related('applicant__profile')

    context = {
        'applications': applications
    }
    return render(request, 'applications/manage_applications.html', context)

@login_required
def accept_application(request, application_id):
    if request.user.role != 'recruiter':
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')

    application = get_object_or_404(Application, id=application_id)

    # Ensure the recruiter is the owner of the job
    if application.job.recruiter != request.user:
        messages.error(request, "You don't have permission to manage this application.")
        return redirect('manage_applications')

    application.status = 'accepted'
    application.save()
    messages.success(request, f"You've accepted {application.applicant.username}'s application.")

    return redirect('manage_applications')

@login_required
def reject_application(request, application_id):
    if request.user.role != 'recruiter':
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')

    application = get_object_or_404(Application, id=application_id)

    # Ensure the recruiter is the owner of the job
    if application.job.recruiter != request.user:
        messages.error(request, "You don't have permission to manage this application.")
        return redirect('manage_applications')

    application.status = 'rejected'
    application.save()
    messages.info(request, f"You've rejected {application.applicant.username}'s application.")

    return redirect('manage_applications')
