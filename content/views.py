# content/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import NewsPost, PublicHoliday, CityClimate, FAQ, SupportTicket
from .serializers import (
    NewsPostSerializer,
    PublicHolidaySerializer,
    CityClimateSerializer,
    FAQSerializer,
    SupportTicketSerializer,
    SupportTicketStatusUpdateSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin


class NewsPostViewSet(viewsets.ModelViewSet):
    """
    GET    /api/news/
    GET    /api/news/{id}/
    POST   /api/news/          (admin only)
    PUT    /api/news/{id}/     (admin only)
    PATCH  /api/news/{id}/     (admin only)
    DELETE /api/news/{id}/     (admin only)
    """
    queryset = NewsPost.objects.all()
    serializer_class = NewsPostSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'city', 'is_active']
    search_fields = ['title', 'summary', 'city']
    ordering_fields = ['published_at', 'created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        # Public (non-admin) users only ever see active posts
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)
        return qs


class PublicHolidayViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Per requirements, no API is strictly required for this model,
    but it's included here as read-only + admin-managed in case
    that decision changes later.

    GET    /api/holidays/
    GET    /api/holidays/{id}/
    POST   /api/holidays/      (admin only)
    PUT    /api/holidays/{id}/ (admin only)
    DELETE /api/holidays/{id}/ (admin only)
    """
    queryset = PublicHoliday.objects.all()
    serializer_class = PublicHolidaySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_national', 'state']
    ordering_fields = ['date']


class CityClimateViewSet(viewsets.ModelViewSet):
    """
    GET    /api/climate/
    GET    /api/climate/{id}/
    POST   /api/climate/          (admin only)
    PUT    /api/climate/{id}/     (admin only)
    DELETE /api/climate/{id}/     (admin only)
    """
    queryset = CityClimate.objects.all()
    serializer_class = CityClimateSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['city']
    filterset_fields = ['city']  # allows /api/climate/Bangalore/ instead of by id


class FAQViewSet(viewsets.ModelViewSet):
    """
    GET    /api/faqs/
    GET    /api/faqs/{id}/
    POST   /api/faqs/          (admin only)
    PUT    /api/faqs/{id}/     (admin only)
    DELETE /api/faqs/{id}/     (admin only)
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering = ['order']

    def get_queryset(self):
        qs = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)
        return qs.order_by('order')


class SupportTicketViewSet(viewsets.ModelViewSet):
    """
    GET    /api/tickets/          (own tickets, or all if admin)
    GET    /api/tickets/{id}/     (owner or admin)
    POST   /api/tickets/          (any authenticated user)
    PATCH  /api/tickets/{id}/     (admin only — status update)
    DELETE /api/tickets/{id}/     (owner or admin)
    """
    queryset = SupportTicket.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return SupportTicket.objects.none()

        user = self.request.user
        if user.is_staff:
            return SupportTicket.objects.all()
        return SupportTicket.objects.filter(user=user)

    def get_serializer_class(self):
        # Restrict updates to a status-only serializer, and only for admins
        if self.action in ('update', 'partial_update'):
            if self.request.user.is_staff:
                return SupportTicketStatusUpdateSerializer
        return SupportTicketSerializer

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Only admins can update ticket status.")
        serializer.save()