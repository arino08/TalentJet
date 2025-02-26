from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm

def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    user_has_applied = False

    if request.user.is_authenticated and request.user.role == 'job_seeker':
        user_has_applied = job.applications.filter(applicant=request.user).exists()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'user_has_applied': user_has_applied
    })

@login_required
def create_job(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # Make sure only the recruiter who created the job can delete it
    if request.user != job.recruiter:
        return redirect('job_list')

    if request.method == 'POST':
        job.delete()
        return redirect('job_list')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})
