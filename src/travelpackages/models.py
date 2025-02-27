from django.db import models
from random import randint, uniform, choice
from django.utils import timezone
import datetime
from decimal import Decimal

def get_random_rating():
    return round(uniform(4.0, 5.0), 1)

def get_random_reviews():
    return randint(100, 500)

def get_default_end_date():
    return timezone.now() + datetime.timedelta(days=365)

class Country(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the country")
    code = models.CharField(max_length=3, help_text="Three letter country code", unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

class TravelPackage(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging')
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German')
    ]

    CATEGORY_CHOICES = [
        ('adventure', 'Adventure'),
        ('luxury', 'Luxury'),
        ('cultural', 'Cultural'),
        ('wildlife', 'Wildlife'),
        ('beach', 'Beach')
    ]

    # Basic package details
    title = models.CharField(max_length=200, help_text="Title of the travel package")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='travel_packages')
    city = models.CharField(max_length=100, help_text="City of the travel package")
    image = models.ImageField(upload_to='packages/', help_text="Image for the travel package")

    # Package specifications
    duration = models.IntegerField(help_text="Duration of the trip in days")
    number_of_people = models.IntegerField(help_text="Recommended number of people")

    # Additional details
    highlights = models.TextField(blank=True, help_text="Key highlights of the package (e.g., 'River Cam / University Colleges')")

    # Ratings and reviews
    rating = models.FloatField(
        help_text="Average rating of the package",
        default=get_random_rating
    )
    reviews_count = models.PositiveIntegerField(
        help_text="Number of reviews",
        default=get_random_reviews
    )

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the package")
    youth_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Date-related fields
    is_always_available = models.BooleanField(
        default=False,
        help_text="If true, package is available year-round regardless of dates"
    )
    available_start_date = models.DateField(
        null=True,
        blank=True,
        default=timezone.now,
        help_text="Leave blank if package is always available"
    )
    available_end_date = models.DateField(
        null=True,
        blank=True,
        default=get_default_end_date,
        help_text="Leave blank if package is always available"
    )
    booking_deadline = models.IntegerField(
        help_text="Days before departure needed to book",
        default=7,
        null=True,
        blank=True
    )

    # Practical details
    amenities = models.JSONField(
        null=True,
        blank=True,
        default=dict,
        help_text="List of amenities included"
    )
    itinerary = models.JSONField(
        null=True,
        blank=True,
        default=dict,
        help_text="Day-wise itinerary details"
    )
    transportation = models.TextField(
        null=True,
        blank=True,
        help_text="Transportation details"
    )
    accommodation = models.TextField(
        null=True,
        blank=True,
        help_text="Accommodation details"
    )

    # Additional information
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='moderate',
        null=True,
        blank=True
    )
    fitness_level = models.IntegerField(
        help_text="Required fitness level (1-5)",
        default=1,
        null=True,
        blank=True
    )
    tour_language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en',
        null=True,
        blank=True
    )
    cancellation_policy = models.TextField(
        null=True,
        blank=True,
        help_text="Cancellation policy details"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='cultural',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Travel Package"
        verbose_name_plural = "Travel Packages"

    def __str__(self):
        return self.title

    def is_available(self, check_date=None):
        if self.is_always_available:
            return True
        if not check_date:
            check_date = timezone.now().date()
        if not self.available_start_date or not self.available_end_date:
            return False
        return self.available_start_date <= check_date <= self.available_end_date

    def get_youth_price(self):
        """Return youth price if set, otherwise return 80% of regular price"""
        if self.youth_price:
            return self.youth_price
        return self.price * Decimal('1')  # you can add discount use 0.8 for 20% discount for youth
