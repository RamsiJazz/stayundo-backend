from django.db import models
from django.contrib.auth.models import User


class HousingCategory(models.Model):
    """Image 1 - Popular Categories (Hostels, Apartments, Villa, PG)"""
    HOUSING_TYPES = [
        ('hostel', 'Hostel'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('pg', 'PG'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    housing_type = models.CharField(max_length=20, choices=HOUSING_TYPES)
    tagline = models.CharField(max_length=200, default='Explore premium listings')
    image = models.ImageField(upload_to='housing_categories/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Housing Categories'

    def __str__(self):
        return self.name


class ExpenseCategory(models.Model):
    """Image 2 - Browse Categories (Accommodation Rent, Daily Food, etc.)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='expense_categories/')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Expense Categories'

    def __str__(self):
        return self.name


