#subscriptions/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import User


class SubscriptionPlan(models.Model):
    PLAN_FOR_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]

    name = models.CharField(max_length=100)               # e.g. "30 Days Plan", "Seller Yearly"
    plan_for = models.CharField(max_length=10, choices=PLAN_FOR_CHOICES)
    duration_days = models.PositiveIntegerField()          # 30, 60, 365
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 199.00, 399.00, 2388.00
    is_free_trial = models.BooleanField(default=False)     # True for seller's 1-month free
    is_active = models.BooleanField(default=True)          # admin can disable a plan
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['plan_for', 'duration_days']

    def __str__(self):
        return f"{self.name} ({self.plan_for}) - ₹{self.price} / {self.duration_days}d"


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions',
    )

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100, blank=True)  # gateway transaction id, later
    used_free_trial = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def is_currently_active(self):
        return self.status == 'active' and self.end_date >= timezone.now()

    def __str__(self):
        return f"{self.user} → {self.plan.name} ({self.status})"