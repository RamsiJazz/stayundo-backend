# content/models.py
from django.db import models
from django.contrib.auth.models import User


class NewsPost(models.Model):
    CATEGORY_CHOICES = [
        ('upcoming', 'Upcoming Event'),
        ('news', 'General News'),
        ('alert', 'Alert'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='news')
    summary = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    source_link = models.URLField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class PublicHoliday(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)
    is_national = models.BooleanField(default=True)
    state = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} – {self.date}"


class CityClimate(models.Model):
    city = models.CharField(max_length=100, unique=True)
    summary = models.TextField(blank=True)
    best_time_to_visit = models.CharField(max_length=100, blank=True)
    banner_image = models.ImageField(upload_to='climate/', null=True, blank=True)
    weather_api_city_key = models.CharField(
        max_length=100, blank=True,
        help_text="City key for OpenWeatherMap API on frontend"
    )

    def __str__(self):
        return self.city


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tickets'
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} – {self.user}"