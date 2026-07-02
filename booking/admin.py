#booking/admin.py
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Booking, BookingStatusLog


class BookingStatusLogInline(admin.TabularInline):
    model = BookingStatusLog
    extra = 0
    readonly_fields = ['changed_by', 'old_status', 'new_status', 'note', 'changed_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tenant', 'listing', 'move_in_date', 'total_amount', 'status', 'payment_status']
    list_filter = ['status', 'payment_status']
    search_fields = ['tenant__email', 'listing__title']
    readonly_fields = ['id', 'rent_amount', 'security_deposit', 'advance_deposit', 'total_amount', 'created_at']
    inlines = [BookingStatusLogInline]


@admin.register(BookingStatusLog)
class BookingStatusLogAdmin(admin.ModelAdmin):
    list_display = ['booking', 'old_status', 'new_status', 'changed_by', 'changed_at']
    readonly_fields = ['booking', 'changed_by', 'old_status', 'new_status', 'changed_at']