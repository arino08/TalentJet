from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Application
from jobs.models import Job

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
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'applications/my_applications.html', {'applications': applications})

@login_required
def manage_applications(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')

    jobs = Job.objects.filter(recruiter=request.user)
    applications = Application.objects.filter(job__in=jobs).order_by('-applied_at')

    return render(request, 'applications/manage_applications.html', {'applications': applications})

@login_required
def accept_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    # Check if user is the recruiter for this job
    if request.user == application.job.recruiter:
        application.status = 'accepted'
        application.save()
    return redirect('job_detail', pk=application.job.pk)

@login_required
def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    # Check if user is the recruiter for this job
    if request.user == application.job.recruiter:
        application.status = 'rejected'
        application.save()
    return redirect('job_detail', pk=application.job.pk)
