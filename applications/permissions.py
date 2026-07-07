# applications/permissions.py
from rest_framework.permissions import BasePermission


class IsApplicant(BasePermission):
    """Only the student who submitted the application can view it."""
    def has_object_permission(self, request, view, obj):
        return obj.applicant == request.user


class IsListingSellerOrAdmin(BasePermission):
    """Only the hostel owner (or admin) can review applications on their listing."""
    def has_object_permission(self, request, view, obj):
        return obj.listing.seller == request.user or request.user.is_staff