# applications/models.py
import uuid
from django.core.exceptions import ValidationError
from django.db import models
from listings.models import Listing
from users.models import User

class HostelApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    ROOM_TYPE_CHOICES = [
        ("single", "Single Sharing"),
        ("double", "Double Sharing"),
        ("triple", "Triple Sharing"),
        ("dormitory", "Dormitory"),
    ]
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hostel_applications"
    )

    # --- Form fields ---
    full_name = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    id_proof = models.FileField(upload_to="applications/id_proofs/", blank=True, null=True)
    duration_months = models.PositiveIntegerField()
    preferred_room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    message = models.TextField(blank=True)  # optional note from applicant

    # --- Review workflow ---
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    review_note = models.TextField(blank=True)          # seller's reason for approve/reject
    payment_details = models.TextField(blank=True)      # shared with student after approval
    admission_details = models.TextField(blank=True)    # move-in date, room no, etc.

    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # Prevent duplicate spam applications, but allow re-applying after rejection
            models.UniqueConstraint(
                fields=["listing", "applicant"],
                condition=models.Q(status="pending"),
                name="unique_pending_application_per_listing",
            )
        ]

    def __str__(self):
        return f"{self.full_name} -> {self.listing.title} ({self.status})"

    def clean(self):
        if self.listing.category.housing_type != "hostel":
            raise ValidationError("Applications can only be submitted for hostel listings.")