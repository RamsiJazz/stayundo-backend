import uuid
from django.db import models
from django.utils import timezone
from listings.models import Listing
from users.models import User


class Coupon(models.Model):

    DISCOUNT_TYPE_CHOICES = [
        ('fixed', 'Fixed Amount'),        # e.g. ₹500 off
        ('percentage', 'Percentage'),     # e.g. 10% off
    ]

    CATEGORY_CHOICES = [
        ('general', 'General'),           # works on any listing
        ('specific', 'Specific Listings'),# works only on selected listings
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # --- Core ---
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255, blank=True)  # e.g. "10% off for new users"

    # --- Discount ---
    discount_type = models.CharField(max_length=15, choices=DISCOUNT_TYPE_CHOICES, default='fixed')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)  # amount or percent
    max_discount_cap = models.DecimalField(                                 # cap for percentage type
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    # --- Category / Scope ---
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    listings = models.ManyToManyField(Listing, related_name='coupons', blank=True)  # used when category=specific

    # --- Duration ---
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # --- Usage Rules ---
    usage_limit = models.PositiveIntegerField(default=1)       # total times it can be used
    used_count = models.PositiveIntegerField(default=0)        # auto incremented on use
    per_user_limit = models.PositiveIntegerField(default=1)    # how many times one user can use

    # --- Status ---
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, related_name='created_coupons'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active
            and self.start_date <= now <= self.end_date
            and self.used_count < self.usage_limit
        )

    def calculate_discount(self, amount):
        """Calculate actual discount for a given amount"""
        if self.discount_type == 'fixed':
            return min(self.discount_value, amount)
        else:  # percentage
            discount = (self.discount_value / 100) * amount
            if self.max_discount_cap:
                discount = min(discount, self.max_discount_cap)
            return round(discount, 2)


class CouponUsage(models.Model):
    """Track who used which coupon — enforces per_user_limit"""
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_usages')
    used_at = models.DateTimeField(auto_now_add=True)
    booking_id = models.UUIDField(blank=True, null=True)   # reference to booking

    class Meta:
        ordering = ['-used_at']

    def __str__(self):
        return f"{self.user} used {self.coupon.code}"