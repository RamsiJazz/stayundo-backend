#coupons/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOnly(BasePermission):
    """Only admin can create/edit/delete coupons"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAdminOrAuthenticatedReadOnly(BasePermission):
    """
    GET  → any authenticated user (buyer/seller)
    POST/PUT/DELETE → admin only
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff