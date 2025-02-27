from django.db import models
from django.conf import settings
from travelpackages.models import TravelPackage

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.CharField(max_length=10)
    adults = models.IntegerField(default=0)
    youth = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    airport_transfer = models.BooleanField(default=False)
    personal_guide = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Contact information fields
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)  # Add this line
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s booking for {self.package.title}"
