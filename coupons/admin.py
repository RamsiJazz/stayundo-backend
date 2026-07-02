#admin.py
from django.contrib import admin
from .models import Coupon, CouponUsage


class CouponUsageInline(admin.TabularInline):
    model = CouponUsage
    extra = 0
    readonly_fields = ['user', 'used_at', 'booking_id']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'category', 'start_date', 'end_date', 'used_count', 'usage_limit', 'is_active']
    list_filter = ['discount_type', 'category', 'is_active']
    search_fields = ['code', 'description']
    filter_horizontal = ['listings']
    readonly_fields = ['used_count', 'created_at']
    inlines = [CouponUsageInline]


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user', 'used_at', 'booking_id']
    readonly_fields = ['coupon', 'user', 'used_at', 'booking_id']