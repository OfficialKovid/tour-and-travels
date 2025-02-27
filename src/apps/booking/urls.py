from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('checkout/', views.checkout, name='checkout'),  # Remove booking_id parameter
    path('complete-booking/', views.complete_booking, name='complete_booking'),
]