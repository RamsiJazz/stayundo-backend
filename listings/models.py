#listings/models.py
import uuid
from django.conf import settings
from django.db import models
from categories.models import HousingCategory


class Listing(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("inactive", "Inactive"),
    ]
    QUALITY_GRADES = [
        ("premium", "Premium"),
        ("standard", "Standard"),
        ("budget", "Budget"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )
    category = models.ForeignKey(
        HousingCategory,
        on_delete=models.PROTECT,
        related_name="listings",
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    quality_grade = models.CharField(max_length=20, choices=QUALITY_GRADES, default="standard")

    # --- Media ---
    cover_image = models.ImageField(upload_to="listings/covers/", blank=True, null=True)

    # --- Location ---
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100)
    google_map_link = models.URLField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # --- Contact ---
    phone = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)

    # --- Pricing ---
    price = models.DecimalField(max_digits=10, decimal_places=2)          # Monthly rent
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # --- Food ---
    food_available = models.BooleanField(default=False)
    food_description = models.CharField(max_length=300, blank=True)
    food_price_per_month = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    # --- Security ---
    SECURITY_CHOICES = [
        ("24x7", "24x7 Security"),
        ("guard", "Security Guard"),
        ("cctv", "CCTV"),
        ("gated", "Gated Community"),
    ]

    security_available = models.BooleanField(default=False)

    security_type = models.CharField(
        max_length=20,
        choices=SECURITY_CHOICES,
        blank=True
    )

    security_details = models.TextField(blank=True)

    # --- Stay Rules ---
    stay_rules = models.TextField(blank=True)   # e.g. "No smoking, No pets"
    gender_preference = models.CharField(
        max_length=10,
        choices=[("any", "Any"), ("male", "Male Only"), ("female", "Female Only")],
        default="any",
    )
    min_stay_months = models.PositiveIntegerField(default=1)

    # --- Flags ---
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # --- Stats ---
    average_rating = models.FloatField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="listings/gallery/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.listing.title} - Image {self.display_order}"


class ListingAmenity(models.Model):
    """Master list of amenities e.g. WiFi, AC, Laundry"""
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True)   # icon class or emoji

    def __str__(self):
        return self.name


class ListingAmenityMapping(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="amenity_mappings")
    amenity = models.ForeignKey(ListingAmenity, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["listing", "amenity"], name="unique_listing_amenity")
        ]

    def __str__(self):
        return f"{self.listing.title} - {self.amenity.name}"


class ListingSpecification(models.Model):
    """
    Flexible key-value for special features.
    e.g. key='Total Beds', value='6'  |  key='Floor', value='2nd'
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="specifications")
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["listing", "key"], name="unique_listing_spec")
        ]
        ordering = ["key"]

    def __str__(self):
        return f"{self.key}: {self.value}"


class ListingOffer(models.Model):
    """
    Seller creates offers on their own listing.
    e.g. "First month 20% off", "Free food for 2 weeks"
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.listing.title} - {self.title}"