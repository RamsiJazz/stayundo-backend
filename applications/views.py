# applications/views.py
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from listings.models import Listing
from .models import HostelApplication
from .serializers import (
    HostelApplicationCreateSerializer,
    HostelApplicationSerializer,
    HostelApplicationReviewSerializer,
)
from .permissions import IsListingSellerOrAdmin, IsApplicant


# ── Student ────────────────────────────────────────────────────

class HostelApplicationCreateView(generics.CreateAPIView):
    """Student: submit 'Apply for stay' form"""
    serializer_class = HostelApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        context['listing'] = get_object_or_404(Listing, pk=self.kwargs['listing_id'])
        return context

class MyApplicationsView(generics.ListAPIView):
    """Student: list own applications (any status)"""
    serializer_class = HostelApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return HostelApplication.objects.none()
        return HostelApplication.objects.filter(applicant=self.request.user)


class MyApplicationDetailView(generics.RetrieveAPIView):
    """Student: check status of one application"""
    serializer_class = HostelApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsApplicant]
    queryset = HostelApplication.objects.all()

    def get_object(self):
        obj = get_object_or_404(HostelApplication, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


# ── Hostel owner (seller) ─────────────────────────────────────

class ListingApplicationListView(generics.ListAPIView):
    """Seller: view applications received on one of their hostel listings"""
    serializer_class = HostelApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return HostelApplication.objects.none()
        listing = get_object_or_404(Listing, slug=self.kwargs['slug'], seller=self.request.user)
        qs = HostelApplication.objects.filter(listing=listing)
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        return qs


class ApplicationReviewView(generics.RetrieveUpdateAPIView):
    """Seller/Admin: approve/reject + share payment/admission details"""
    permission_classes = [permissions.IsAuthenticated, IsListingSellerOrAdmin]
    queryset = HostelApplication.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return HostelApplicationSerializer
        return HostelApplicationReviewSerializer

    def get_object(self):
        obj = get_object_or_404(HostelApplication, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
