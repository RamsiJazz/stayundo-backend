#listings/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBuyer(BasePermission):
    """Authenticated non-seller, non-admin user"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_staff


class IsSeller(BasePermission):
    """Any authenticated user acting as seller (owns a listing)"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsSellerOrAdmin(BasePermission):
    """Write: only listing owner or admin. Read: anyone."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.seller == request.user or request.user.is_staff


class IsListingSellerOrAdmin(BasePermission):
    """For sub-resources (images, specs, offers) — checks parent listing seller"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj is a sub-resource with a .listing FK
        return obj.listing.seller == request.user or request.user.is_staff


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff