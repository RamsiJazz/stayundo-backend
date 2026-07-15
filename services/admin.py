#services/admin.py
from django.contrib import admin
from .models import Service, ServiceCategory, MessRestaurantDetail, TransportDetail, HospitalDetail, AttractionDetail, EducationDetail, SecurityDetail


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'is_active']
    list_filter = ['service_type', 'is_active']


class MessRestaurantDetailInline(admin.StackedInline):
    model = MessRestaurantDetail
    extra = 0


class TransportDetailInline(admin.StackedInline):
    model = TransportDetail
    extra = 0


class HospitalDetailInline(admin.StackedInline):
    model = HospitalDetail
    extra = 0

class AttractionDetailInline(admin.StackedInline):  
    model = AttractionDetail
    extra = 0

class SecurityDetailInline(admin.StackedInline):  
    model = SecurityDetail
    extra = 0
class EducationDetailInline(admin.StackedInline):  
    model = EducationDetail
    extra = 0


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'city', 'is_verified', 'is_active', 'created_at']
    list_filter = ['category__service_type', 'is_verified', 'is_active', 'city']
    search_fields = ['name', 'city']
    fields = ['name', 'description', 'image', 'category', 'phone', 'maps_link', 'city', 'is_verified', 'is_active']
    inlines = [MessRestaurantDetailInline, TransportDetailInline, HospitalDetailInline, AttractionDetailInline, SecurityDetailInline, EducationDetailInline]