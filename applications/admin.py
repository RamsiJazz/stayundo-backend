# applications/admin.py
from django.contrib import admin
from .models import HostelApplication


@admin.register(HostelApplication)
class HostelApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'listing', 'applicant', 'gender',
        'preferred_room_type', 'duration_months',
        'status', 'created_at', 'reviewed_at',
    ]
    list_filter = ['status', 'gender', 'preferred_room_type', 'created_at']
    search_fields = [
        'full_name', 'applicant__email', 'applicant__username',
        'listing__title', 'listing__slug',
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_select_related = ['listing', 'applicant']

    readonly_fields = ['id', 'created_at', 'updated_at', 'reviewed_at']

    fieldsets = (
        ('Application Info', {
            'fields': ('id', 'listing', 'applicant', 'status')
        }),
        ('Applicant Details', {
            'fields': ('full_name', 'age', 'gender', 'id_proof')
        }),
        ('Stay Preferences', {
            'fields': ('duration_months', 'preferred_room_type', 'message')
        }),
        ('Review', {
            'fields': ('review_note', 'payment_details', 'admission_details')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'reviewed_at')
        }),
    )

    actions = ['approve_applications', 'reject_applications']

    @admin.action(description="Approve selected applications")
    def approve_applications(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='approved', reviewed_at=timezone.now())
        self.message_user(request, f"{updated} application(s) approved.")

    @admin.action(description="Reject selected applications")
    def reject_applications(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='rejected', reviewed_at=timezone.now())
        self.message_user(request, f"{updated} application(s) rejected.")