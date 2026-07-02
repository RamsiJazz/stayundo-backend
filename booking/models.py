#booking/models.py
from django.db import models

# Create your models here.
import uuid
from django.conf import settings
from django.db import models
from listings.models import Listing


class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),        # just submitted
        ('confirmed', 'Confirmed'),    # seller/admin confirmed
        ('cancelled', 'Cancelled'),    # cancelled by user or seller
        ('completed', 'Completed'),    # stay completed
        ('rejected', 'Rejected'),      # seller rejected
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),        # advance paid
        ('paid', 'Paid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name='bookings')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')

    # --- Stay Duration ---
    move_in_date = models.DateField()
    move_out_date = models.DateField(blank=True, null=True)   # optional for long stays
    duration_months = models.PositiveIntegerField(default=1)

    # --- Pricing Snapshot (at time of booking) ---
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    food_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # --- Coupon ---
    coupon_code = models.CharField(max_length=20, blank=True)

    # --- Status ---
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    # --- Notes ---
    tenant_note = models.TextField(blank=True)     # message from tenant
    seller_note = models.TextField(blank=True)     # response from seller

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tenant} → {self.listing.title} ({self.status})"


class BookingStatusLog(models.Model):
    """Track every status change for audit trail"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='status_logs')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    note = models.CharField(max_length=300, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.booking.id} | {self.old_status} → {self.new_status}"