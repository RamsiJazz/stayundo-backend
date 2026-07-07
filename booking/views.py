#booking.views.py
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Booking, BookingStatusLog
from .serializers import (
    BookingCreateSerializer, BookingListSerializer, BookingDetailSerializer,
    BookingStatusUpdateSerializer, BookingSellerNoteSerializer,
)
from .permissions import IsTenantOrAdmin, IsListingSellerOrAdmin, IsTenantOrSellerOrAdmin


# ── Tenant ────────────────────────────────────────────────────────────────────

class BookingCreateView(generics.CreateAPIView):
    """Tenant: submit a booking"""
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyBookingsView(generics.ListAPIView):
    """Tenant: see own bookings"""
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        return Booking.objects.filter(tenant=self.request.user)


class MyBookingDetailView(generics.RetrieveAPIView):
    """Tenant: full detail of own booking"""
    serializer_class = BookingDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantOrAdmin]
    lookup_field = 'id'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        return Booking.objects.all()


class BookingCancelView(APIView):
    """Tenant: cancel own booking (only if pending)"""
    permission_classes = [permissions.IsAuthenticated, IsTenantOrAdmin]

    def patch(self, request, id):
        booking = get_object_or_404(Booking, id=id, tenant=request.user)
        self.check_object_permissions(request, booking)

        if booking.status not in ['pending', 'confirmed']:
            return Response(
                {"detail": "Cannot cancel at this stage."},
                status=status.HTTP_400_BAD_REQUEST
            )

        old_status = booking.status
        booking.status = 'cancelled'
        booking.save(update_fields=['status'])

        BookingStatusLog.objects.create(
            booking=booking,
            changed_by=request.user,
            old_status=old_status,
            new_status='cancelled',
            note='Cancelled by tenant',
        )

        return Response({"detail": "Booking cancelled."})


# ── Seller ────────────────────────────────────────────────────────────────────

class SellerBookingsView(generics.ListAPIView):
    """Seller: see all bookings for their listings"""
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        return Booking.objects.filter(listing__seller=self.request.user)


class SellerBookingDetailView(generics.RetrieveAPIView):
    """Seller: full detail of a booking on their listing"""
    serializer_class = BookingDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsListingSellerOrAdmin]
    lookup_field = 'id'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        return Booking.objects.all()


class SellerBookingStatusView(APIView):
    """Seller: confirm or reject a booking"""
    permission_classes = [permissions.IsAuthenticated, IsListingSellerOrAdmin]

    def patch(self, request, id):
        booking = get_object_or_404(Booking, id=id)
        self.check_object_permissions(request, booking) 

        serializer = BookingStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        note = serializer.validated_data.get('note', '')

        # Seller can only confirm or reject
        if new_status not in ['confirmed', 'rejected']:
            return Response(
                {"detail": "Seller can only confirm or reject."},
                status=status.HTTP_400_BAD_REQUEST
            )

        old_status = booking.status
        booking.status = new_status
        booking.save(update_fields=['status'])

        BookingStatusLog.objects.create(
            booking=booking,
            changed_by=request.user,
            old_status=old_status,
            new_status=new_status,
            note=note,
        )

        return Response({"detail": f"Booking {new_status}.", "status": new_status})


class SellerBookingNoteView(generics.UpdateAPIView):
    """Seller: add a note to a booking"""
    serializer_class = BookingSellerNoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsListingSellerOrAdmin]
    lookup_field = 'id'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        return Booking.objects.all()


# ── Admin ─────────────────────────────────────────────────────────────────────

class AdminBookingListView(generics.ListAPIView):
    """Admin: all bookings"""
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Booking.objects.all()


class AdminBookingDetailView(generics.RetrieveAPIView):
    """Admin: any booking detail"""
    serializer_class = BookingDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Booking.objects.all()
    lookup_field = 'id'


class AdminBookingStatusView(APIView):
    """Admin: change any booking to any status"""
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, id):
        booking = get_object_or_404(Booking, id=id)
        serializer = BookingStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_status = booking.status
        new_status = serializer.validated_data['status']
        note = serializer.validated_data.get('note', '')

        booking.status = new_status
        booking.save(update_fields=['status'])

        BookingStatusLog.objects.create(
            booking=booking,
            changed_by=request.user,
            old_status=old_status,
            new_status=new_status,
            note=note,
        )

        return Response({"detail": f"Booking {new_status}.", "status": new_status})