from django.shortcuts import render
from django.db.models import Q, Count
from jobs.models import Job
from django.db.models.functions import Lower

def home(request):
    # Get companies with job counts
    top_companies = Job.objects.values('company') \
                              .annotate(job_count=Count('id')) \
                              .order_by('-job_count')[:10]

    # Format company data for template
    company_data = []
    for company in top_companies:
        company_name = company['company']
        if company_name:  # Skip empty company names
            company_data.append({
                'name': company_name,
                'job_count': company['job_count'],
                'logo_url': None,  # You can improve this by adding logo handling
            })

    # If there are fewer than 5 companies, add some placeholders
    if len(company_data) < 5:
        sample_companies = [
            {'name': 'TechCorp', 'job_count': 12},
            {'name': 'GlobalSoft', 'job_count': 8},
            {'name': 'InnovateTech', 'job_count': 15},
            {'name': 'DataDynamics', 'job_count': 7},
            {'name': 'FutureSystems', 'job_count': 10}
        ]

        # Add needed number of sample companies
        for i in range(min(5 - len(company_data), len(sample_companies))):
            company_data.append({
                'name': sample_companies[i]['name'],
                'job_count': sample_companies[i]['job_count'],
                'logo_url': None
            })

    return render(request, 'home.html', {'top_companies': company_data})

def search_results(request):
    """
    Search view that processes query parameters and returns matching jobs
    """
    search_query = request.GET.get('q', '')

    if search_query:
        # Search across multiple fields
        results = Job.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(required_skills__icontains=search_query)
        ).order_by('-posted_at')
    else:
        # If no query, show all jobs
        results = Job.objects.all().order_by('-posted_at')

    context = {
        'search_query': search_query,
        'results': results,
    }

    return render(request, 'search/search_results.html', context)
