#emergency.models

from django.db import models

class EmergencyContact(models.Model):
    TYPE_CHOICES = (
        ("police", "Police"),
        ("pink_police", "Pink Police"),   # ← add
        ("hospital", "Hospital"),
        ("fire", "Fire Station"),
        ("embassy", "Embassy"),
        ("ambulance", "Ambulance"),   # ← added
        ("pharmacy", "Pharmacy"),     # ← added
        ("drug_helpline", "Drug Helpline"),
    )

    name = models.CharField(max_length=255)
    contact_type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # ← renamed from type

    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)     # ← added
    website = models.URLField(blank=True)     # ← added

    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)

    maps_link = models.URLField(blank=True, help_text="Google Maps URL")

    is_active = models.BooleanField(default=True)     # ← added
    is_verified = models.BooleanField(default=False)  # ← added
    is_24_hours = models.BooleanField(default=False)  # ← added

    created_at = models.DateTimeField(auto_now_add=True)  # ← added
    updated_at = models.DateTimeField(auto_now=True)      # ← added

    def __str__(self):
        return f"{self.name} ({self.contact_type}) - {self.city}"