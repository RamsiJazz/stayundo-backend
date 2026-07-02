#booking.permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTenantOrAdmin(BasePermission):
    """Only the tenant who made the booking or admin"""
    def has_object_permission(self, request, view, obj):
        return obj.tenant == request.user or request.user.is_staff


class IsListingSellerOrAdmin(BasePermission):
    """Only the seller of the listing or admin"""
    def has_object_permission(self, request, view, obj):
        return obj.listing.seller == request.user or request.user.is_staff


class IsTenantOrSellerOrAdmin(BasePermission):
    """Tenant, listing seller, or admin"""
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.tenant == user or
            obj.listing.seller == user or
            user.is_staff
        )