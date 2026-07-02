from django.contrib import admin
from .models import Listing, ListingImage, ListingAmenity, ListingAmenityMapping, ListingSpecification, ListingOffer


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


class ListingSpecInline(admin.TabularInline):
    model = ListingSpecification
    extra = 1


class ListingAmenityInline(admin.TabularInline):
    model = ListingAmenityMapping
    extra = 1


class ListingOfferInline(admin.TabularInline):
    model = ListingOffer
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'city', 'status', 'is_verified', 'is_featured', 'is_active']
    list_filter = ['status', 'is_verified', 'is_featured', 'is_active', 'quality_grade', 'gender_preference']
    search_fields = ['title', 'city', 'address']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_verified', 'is_featured', 'is_active']
    inlines = [ListingImageInline, ListingSpecInline, ListingAmenityInline, ListingOfferInline]


@admin.register(ListingAmenity)
class ListingAmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']