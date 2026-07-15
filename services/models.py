#services/models.py
import uuid
from django.db import models


class ServiceCategory(models.Model):
    SERVICE_TYPES = [
        ('restaurant', 'Restaurant'),
        ('mess', 'Private Mess'),
        ('taxi', 'Taxi/Auto Service'),
        ('bus_train', 'Bus & Train'),
        ('hospital', 'Hospital'),
        ('medical_shop', 'Medical Shop'),
        ('supermarket', 'Supermarket'),
        ('atm_banking', 'ATM & Banking'),
        ('attraction', 'Attraction'),
        ('security', 'Security & Police'),
        ('ambulance', 'Ambulance'),
        ('education', 'Education Institute'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100, unique=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='other')
    icon = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL,
        null=True, related_name='services'
    )
    description = models.TextField(blank=True, help_text="Short note Maps won't tell you, e.g. '24/7 govt hospital, 2km from campus'")
    image = models.URLField(blank=True, help_text="Firebase Storage URL")
    phone = models.CharField(max_length=30, blank=True)
    maps_link = models.URLField(blank=True, help_text="Google Maps URL")
    city = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MessRestaurantDetail(models.Model):
    """Only for restaurants/mess — info Maps won't tell students"""
    FOOD_TYPE_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
        ('both', 'Both'),
    ]
    service = models.OneToOneField(
        Service, on_delete=models.CASCADE, related_name='mess_detail'
    )
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES, default='both')
    meal_times = models.CharField(
        max_length=200, blank=True,
        help_text="e.g. Breakfast 7-10am, Lunch 12-3pm, Dinner 7-10pm"
    )
    is_mess = models.BooleanField(default=False)
    monthly_plan_available = models.BooleanField(default=False)
    monthly_rate = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    menu_image = models.URLField(blank=True, help_text="Firebase Storage URL — menu photo")

    def __str__(self):
        return f"Mess/Restaurant detail – {self.service.name}"


class TransportDetail(models.Model):
    """Local auto/taxi fare info — Maps shows routes but not local rates"""
    TRANSPORT_TYPE_CHOICES = [
        ('taxi', 'Taxi'),
        ('auto', 'Auto Rickshaw'),
        ('bike', 'Bike Taxi'),
    ]
    service = models.OneToOneField(
        Service, on_delete=models.CASCADE, related_name='transport_detail'
    )
    transport_type = models.CharField(max_length=10, choices=TRANSPORT_TYPE_CHOICES)
    base_fare = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    per_km_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_24_7 = models.BooleanField(default=False)
    availability_hours = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Transport detail – {self.service.name}"


class HospitalDetail(models.Model):
    """Emergency info upfront — faster than opening Maps"""
    service = models.OneToOneField(
        Service, on_delete=models.CASCADE, related_name='hospital_detail'
    )
    has_emergency = models.BooleanField(default=False)
    is_24_7 = models.BooleanField(default=False)
    ambulance_number = models.CharField(max_length=30, blank=True)
    specializations = models.CharField(
        max_length=255, blank=True,
        help_text="e.g. Cardiology, Orthopaedics"
    )

    def __str__(self):
        return f"Hospital detail – {self.service.name}"

class AttractionDetail(models.Model):
    ATTRACTION_TYPES = [
        ('theatre', 'Film Theatre'),
        ('railway_station', 'Railway Station'),
        ('mall', 'Mall'),
        ('park', 'Park'),
        ('museum', 'Museum'),
        ('temple', 'Temple/Religious Site'),
        ('other', 'Other'),
    ]
    service = models.OneToOneField(
        Service, on_delete=models.CASCADE, related_name='attraction_detail'
    )
    attraction_type = models.CharField(max_length=20, choices=ATTRACTION_TYPES)
    entry_fee = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Leave blank if free entry"
    )
    is_free = models.BooleanField(default=False)
    opening_hours = models.CharField(
        max_length=100, blank=True, help_text="e.g. 9am – 9pm"
    )
    is_24_7 = models.BooleanField(default=False)

    def __str__(self):
        return f"Attraction detail – {self.service.name}"

class SecurityDetail(models.Model):
    SECURITY_TYPES = [
        ('police', 'Police Station'),
        ('pink_police', 'Pink Police'),
        ('fire', 'Fire Station'),
    ]
    service = models.OneToOneField(
        Service, on_delete=models.CASCADE, related_name='security_detail'
    )
    security_type = models.CharField(max_length=20, choices=SECURITY_TYPES)
    emergency_number = models.CharField(max_length=30, blank=True)
    is_24_7 = models.BooleanField(default=True)

    def __str__(self):
        return f"Security detail – {self.service.name}"


class EducationDetail(models.Model):
    INSTITUTE_TYPES = [
        ('school', 'School'),
        ('college', 'College'),
        ('university', 'University'),
        ('coaching', 'Coaching Center'),
        ('other', 'Other'),
    ]
    service = models.OneToOneField(
        Service, on_delete=models.CASCADE, related_name='education_detail'
    )
    institute_type = models.CharField(max_length=20, choices=INSTITUTE_TYPES)
    courses_offered = models.CharField(
        max_length=255, blank=True,
        help_text="e.g. Engineering, Medical, Arts"
    )
    is_government = models.BooleanField(default=False)
    established_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Education detail – {self.service.name}"