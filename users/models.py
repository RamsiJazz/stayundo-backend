#users/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class User(models.Model):    
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]
    firebase_uid = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    profile_image = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
                        # <-- NEW
    @property
    def is_active(self):
        return True

    @property
    def is_staff(self):
        return self.role == 'admin'

    @property
    def is_superuser(self):
        return self.role == 'admin'

    def __str__(self):
        return self.firebase_uid
    
class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
        null= True,
        blank = True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.firebase_uid} - {self.product}"    
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")

    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
        blank=True,
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]   # ← added: enforce 1–5
    )
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "listing")

    def __str__(self):
        return f"{self.user.firebase_uid} - {self.rating}"
def _recalculate_listing_rating(listing):
    if listing is None:
        return
    stats = listing.reviews.aggregate(avg=Avg('rating'), count=Count('id'))
    listing.average_rating = round(stats['avg'] or 0, 2)
    listing.total_reviews = stats['count'] or 0
    listing.save(update_fields=['average_rating', 'total_reviews'])


@receiver(post_save, sender=Review)
def review_saved(sender, instance, **kwargs):
    _recalculate_listing_rating(instance.listing)


@receiver(post_delete, sender=Review)
def review_deleted(sender, instance, **kwargs):
    _recalculate_listing_rating(instance.listing)