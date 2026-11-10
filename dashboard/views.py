from django.shortcuts import render, redirect
from harvest.models import BorealisDataset
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from harvest.tasks import run_all_sources

def home_view(request):
    return render(request, 'dashboard/home.html')

def stats_view(request):
    total = BorealisDataset.objects.count()
    by_year = BorealisDataset.objects.values('publication_date__year').annotate(count=Count('id'))
    return render(request, 'dashboard/stats.html', {
        'total': total,
        'by_year': by_year,
    })


@staff_member_required
@require_POST
def moissonner_view(request):
    run_all_sources()
    return redirect('home')


def borealis_view(request):
    query = request.GET.get('q', '')
    datasets = BorealisDataset.search(query)
    return render(request, 'dashboard/borealis.html', {
        'datasets': datasets,
        'query': query
    })
