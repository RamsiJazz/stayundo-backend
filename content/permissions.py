#content/permissions.py

# content/permissions.py
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Anyone can read (GET, HEAD, OPTIONS).
    Only admin/staff users can create, update, or delete.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Used for SupportTicket.
    - Admin/staff can access any ticket.
    - Regular users can only access their own ticket.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user_id == request.user.id


class IsAdminForStatusUpdate(permissions.BasePermission):
    """
    Only admin/staff can update the 'status' field of a SupportTicket.
    Regular users can still create/view their own tickets (handled elsewhere).
    """
    def has_permission(self, request, view):
        if request.method in ('PATCH', 'PUT'):
            return bool(request.user and request.user.is_staff)
        return True