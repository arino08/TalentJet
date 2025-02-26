from django.shortcuts import render
from jobs.models import Job
from users.models import CustomUser
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

def search_results(request):
    query = request.GET.get('q', '')
    job_type = request.GET.get('job_type', '')
    experience_level = request.GET.get('experience_level', '')
    location = request.GET.get('location', '')

    jobs = Job.objects.all()
    companies = CustomUser.objects.filter(role='recruiter')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(required_skills__icontains=query)
        )
        companies = companies.filter(
            Q(company__icontains=query) |
            Q(posted_jobs__required_skills__icontains=query)
        ).distinct()

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if experience_level:
        jobs = jobs.filter(experience_level=experience_level)

    if location:
        jobs = jobs.filter(location__icontains=location)

    context = {
        'query': query,
        'jobs': jobs,
        'companies': companies,
        'job_type': job_type,
        'experience_level': experience_level,
        'location': location,
        'total_results': jobs.count(),
    }

    return render(request, 'search_results.html', context)
