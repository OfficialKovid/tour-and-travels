from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from travelpackages.models import TravelPackage
from decimal import Decimal
from datetime import date

# Remove Razorpay imports and initialization

def create_booking(request):
    if request.method == 'POST':
        try:
            package_id = request.POST.get('package_id')
            package = TravelPackage.objects.get(id=package_id)
            total_price = request.POST.get('total_price')
            
            if not total_price or float(total_price) <= 0:
                raise ValueError("Invalid total price")
            
            # Store booking data in session
            booking_data = {
                'package_id': package_id,
                'booking_date': request.POST.get('booking_date'),
                'booking_time': request.POST.get('booking_time'),
                'adults': int(request.POST.get('adults', 0)),
                'youth': int(request.POST.get('youth', 0)),
                'children': int(request.POST.get('children', 0)),
                'airport_transfer': 'transfer' in request.POST.getlist('services[]', []),
                'personal_guide': 'guide' in request.POST.getlist('services[]', []),
                'total_price': total_price,
            }
            request.session['booking_data'] = booking_data
            
            # Check if user is authenticated
            if not request.user.is_authenticated:
                # Store the next URL in session and redirect with next parameter
                return redirect(f'/login/?next=checkout')
            
            return redirect('checkout')
        except (ValueError, TravelPackage.DoesNotExist) as e:
            messages.error(request, "Error processing booking. Please try again.")
            return redirect('packages')
    return redirect('packages')

@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

def package_detail(request, package_id):
    package = TravelPackage.objects.get(id=package_id)
    context = {
        'package': package,
        'today': date.today(),  # Add today's date to context
    }
    return render(request, 'travelpackages/packagedetails.html', context)

@login_required(login_url='login')
def checkout(request):
    booking_data = request.session.get('booking_data')
    if not booking_data:
        messages.error(request, "No booking information found.")
        return redirect('packages')
    
    package = get_object_or_404(TravelPackage, id=booking_data['package_id'])
    
    context = {
        'package': package,
        'booking_date': booking_data['booking_date'],
        'booking_time': booking_data['booking_time'],
        'adults': booking_data['adults'],
        'youth': booking_data['youth'],
        'children': booking_data['children'],
        'airport_transfer': booking_data['airport_transfer'],
        'personal_guide': booking_data['personal_guide'],
        'total_price': Decimal(booking_data['total_price']),
        'base_price': package.price,
        'guests_total': (booking_data['adults'] * package.price) + 
                       (booking_data['youth'] * package.get_youth_price()),
        'services_total': calculate_services_total_from_data(booking_data),
    }
    
    return render(request, 'booking/checkout.html', context)

@login_required(login_url='login')
def complete_booking(request):
    if request.method == 'POST':
        booking_data = request.session.get('booking_data')
        if not booking_data:
            messages.error(request, "No booking information found.")
            return redirect('packages')
            
        package = get_object_or_404(TravelPackage, id=booking_data['package_id'])
        
        # Create the booking only when the form is submitted
        booking = Booking.objects.create(
            user=request.user,
            package=package,
            booking_date=booking_data['booking_date'],
            booking_time=booking_data['booking_time'],
            adults=booking_data['adults'],
            youth=booking_data['youth'],
            children=booking_data['children'],
            airport_transfer=booking_data['airport_transfer'],
            personal_guide=booking_data['personal_guide'],
            total_price=Decimal(booking_data['total_price']),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            is_completed=True,
            payment_method='cash'
        )
        
        # Clear the session data
        del request.session['booking_data']
        
        return render(request, 'booking/booking_success.html', {'booking': booking})
    
    return redirect('packages')

def calculate_services_total(booking):
    total = 0
    if booking.airport_transfer:
        total += 30  # Fixed price for airport transfer
    if booking.personal_guide:
        total += 50 * (booking.adults + booking.youth)  # $50 per person
    return total

def calculate_services_total_from_data(booking_data):
    total = 0
    if booking_data['airport_transfer']:
        total += 30
    if booking_data['personal_guide']:
        total += 50 * (booking_data['adults'] + booking_data['youth'])
    return total

# Remove initiate_payment and payment_callback views