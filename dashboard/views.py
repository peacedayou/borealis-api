from django.shortcuts import render, redirect
from harvest.models import Dataset, BorealisDataset
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
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


@csrf_exempt
def moissonner_view(request):
    if request.method == 'POST':
        run_all_sources()
        return redirect('home')


def borealis_view(request):
    query = request.GET.get('q', '')
    if query:
        datasets = BorealisDataset.objects.filter(
            title__icontains=query
        ) | BorealisDataset.objects.filter(
            description__icontains=query
        ) | BorealisDataset.objects.filter(
            keywords__icontains=query
        )
    else:
        datasets = BorealisDataset.objects.all()
    return render(request, 'dashboard/borealis.html', {
        'datasets': datasets,
        'query': query
    })
