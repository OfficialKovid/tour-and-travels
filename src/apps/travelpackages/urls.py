from django.urls import path
from .views import *

urlpatterns = [
    path('packages/', packages, name='travelpackages/packages'),
    path('package/<int:package_id>/', package_detail, name='package_detail'),
    path('packages/country/<str:country>/', packages_by_country, name='packages_by_country'),
    path('search/', search_packages, name='search_packages'),  # Add this new URL
]