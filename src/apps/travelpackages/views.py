from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import TravelPackage, Country
from django.db.models import Q

def packages(request):
    packages = TravelPackage.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        packages = packages.filter(
            Q(title__icontains=search_query) |
            Q(country__name__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        packages = packages.filter(price__gte=min_price)
    if max_price:
        packages = packages.filter(price__lte=max_price)
    
    # Duration filter
    duration = request.GET.get('duration')
    if duration:
        if duration == '1-3':
            packages = packages.filter(duration__lte=3)
        elif duration == '4-7':
            packages = packages.filter(duration__range=(4, 7))
        elif duration == '8+':
            packages = packages.filter(duration__gte=8)
    
    # Category filter
    category = request.GET.get('category')
    if category:
        packages = packages.filter(category=category)
    
    # Rating filter
    rating = request.GET.get('rating')
    if rating:
        packages = packages.filter(rating__gte=float(rating))
    
    # Sorting
    sort = request.GET.get('sort')
    if sort:
        if sort == 'price_asc':
            packages = packages.order_by('price')
        elif sort == 'price_desc':
            packages = packages.order_by('-price')
        elif sort == 'rating':
            packages = packages.order_by('-rating')
        elif sort == 'duration':
            packages = packages.order_by('duration')

    context = {
        'packages': packages,
        'categories': TravelPackage.CATEGORY_CHOICES,
        'selected_categories': request.GET.getlist('category'),
    }
    return render(request, 'travelpackages/packages.html', context)

def package_detail(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    return render(request, 'travelpackages/packagedetails.html', {'package': package})

def packages_by_country(request, country):
    # Get the country object first
    country_obj = get_object_or_404(Country, name__iexact=country)
    # Then filter packages by country
    packages = TravelPackage.objects.filter(country=country_obj)
    return render(request, 'travelpackages/packages.html', {
        'packages': packages,
        'country': country
    })

def search_packages(request):
    packages = TravelPackage.objects.all()
    # Get all countries for the filter dropdown
    countries = Country.objects.all().order_by('name')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        packages = packages.filter(
            Q(title__icontains=search_query) |
            Q(country__name__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        packages = packages.filter(price__gte=min_price)
    if max_price:
        packages = packages.filter(price__lte=max_price)
    
    # Duration filter
    duration = request.GET.getlist('duration')
    if duration:
        duration_queries = Q()
        for dur in duration:
            if dur == '1-3':
                duration_queries |= Q(duration__lte=3)
            elif dur == '4-7':
                duration_queries |= Q(duration__range=(4, 7))
            elif dur == '8+':
                duration_queries |= Q(duration__gte=8)
        packages = packages.filter(duration_queries)
    
    # Category filter
    categories = request.GET.getlist('category')
    if categories:
        packages = packages.filter(category__in=categories)
    
    # Country filter
    selected_country = request.GET.get('country')
    if selected_country:
        packages = packages.filter(country__name__iexact=selected_country)
    
    # Rating filter
    rating = request.GET.get('rating')
    if rating:
        packages = packages.filter(rating__gte=float(rating))
    
    # Sorting
    sort = request.GET.get('sort')
    if sort:
        if sort == 'price_asc':
            packages = packages.order_by('price')
        elif sort == 'price_desc':
            packages = packages.order_by('-price')
        elif sort == 'rating':
            packages = packages.order_by('-rating')
        elif sort == 'duration':
            packages = packages.order_by('duration')

    context = {
        'packages': packages,
        'categories': TravelPackage.CATEGORY_CHOICES,
        'countries': countries,  # Add countries to context
        'selected_categories': categories or [],
        'selected_country': selected_country or '',  # Add selected country
        'search_query': search_query or '',
        'min_price': min_price or '',
        'max_price': max_price or '',
        'selected_duration': duration or [],
        'selected_sort': sort or '',
    }
    return render(request, 'travelpackages/search.html', context)