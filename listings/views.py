#listings.views.py
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Listing, ListingImage, ListingAmenity,
    ListingAmenityMapping, ListingSpecification, ListingOffer
)
from .serializers import (
    ListingListSerializer, ListingDetailSerializer, ListingWriteSerializer,
    ListingImageSerializer, ListingAmenitySerializer, ListingAmenityMappingSerializer,
    ListingSpecificationSerializer, ListingOfferSerializer,
)
from .permissions import IsSellerOrAdmin, IsAdminOnly, IsListingSellerOrAdmin
from .filters import ListingFilter


# ── Public / Buyer ────────────────────────────────────────────────────────────

class ListingListView(generics.ListAPIView):
    """Public + Buyer: browse published listings"""
    serializer_class = ListingListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ListingFilter                                   # fixed: use filterset_class
    search_fields = ['title', 'address', 'city', 'description']
    ordering_fields = ['price', 'average_rating', 'created_at']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Listing.objects.none()
        return Listing.objects.filter(status='published', is_active=True)


class ListingDetailView(generics.RetrieveAPIView):
    """Public + Buyer: full listing detail, auto-increments views"""
    serializer_class = ListingDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Listing.objects.none()
        return Listing.objects.filter(status='published', is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.total_views += 1
        instance.save(update_fields=['total_views'])
        return super().retrieve(request, *args, **kwargs)


# ── Seller ────────────────────────────────────────────────────────────────────

class ListingCreateView(generics.CreateAPIView):
    """Seller: create a new listing (starts as draft)"""
    serializer_class = ListingWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ListingUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Seller: edit/delete own listing | Admin: edit/delete any"""
    serializer_class = ListingWriteSerializer
    permission_classes = [IsSellerOrAdmin]
    lookup_field = 'slug'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Listing.objects.none()
        return Listing.objects.all()
    def get_object(self):
        obj = get_object_or_404(
            Listing,
            slug=self.kwargs["slug"]
        )
        self.check_object_permissions(self.request, obj)
        return obj


class MyListingsView(generics.ListAPIView):
    """Seller: see own listings (all statuses)"""
    serializer_class = ListingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Listing.objects.none()
        return Listing.objects.filter(seller=self.request.user)


# ── Images ────────────────────────────────────────────────────────────────────

class ListingImageUploadView(generics.CreateAPIView):
    """Seller: upload images to own listing"""
    serializer_class = ListingImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        listing = get_object_or_404(Listing, slug=self.kwargs['slug'], seller=self.request.user)
        serializer.save(listing=listing)


class ListingImageDeleteView(generics.DestroyAPIView):
    """Seller/Admin: delete an image"""
    permission_classes = [IsListingSellerOrAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ListingImage.objects.none()
        return ListingImage.objects.filter(listing__slug=self.kwargs['slug'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


# ── Amenities (Master list) ───────────────────────────────────────────────────

class AmenityListCreateView(generics.ListCreateAPIView):
    """GET: public | POST: admin only"""
    serializer_class = ListingAmenitySerializer
    queryset = ListingAmenity.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsAdminOnly()]


# ── Amenity Mapping ───────────────────────────────────────────────────────────

class ListingAmenityAddView(generics.CreateAPIView):
    """Seller: add amenity to own listing"""
    serializer_class = ListingAmenityMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        listing = get_object_or_404(Listing, slug=self.kwargs['slug'], seller=self.request.user)
        serializer.save(listing=listing)


class ListingAmenityRemoveView(generics.DestroyAPIView):
    """Seller/Admin: remove amenity from listing"""
    permission_classes = [IsListingSellerOrAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ListingAmenityMapping.objects.none()
        return ListingAmenityMapping.objects.filter(listing__slug=self.kwargs['slug'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


# ── Specifications ────────────────────────────────────────────────────────────

class ListingSpecListCreateView(generics.ListCreateAPIView):
    """GET: public | POST: seller only"""
    serializer_class = ListingSpecificationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ListingSpecification.objects.none()
        return ListingSpecification.objects.filter(listing__slug=self.kwargs['slug'])

    def perform_create(self, serializer):
        listing = get_object_or_404(Listing, slug=self.kwargs['slug'], seller=self.request.user)
        serializer.save(listing=listing)


class ListingSpecDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Seller/Admin: edit or delete a spec"""
    serializer_class = ListingSpecificationSerializer
    permission_classes = [IsListingSellerOrAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ListingSpecification.objects.none()
        return ListingSpecification.objects.filter(listing__slug=self.kwargs['slug'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


# ── Offers ────────────────────────────────────────────────────────────────────

class ListingOfferListCreateView(generics.ListCreateAPIView):
    """GET: public (buyers see offers) | POST: seller only"""
    serializer_class = ListingOfferSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return ListingOffer.objects.filter(
            listing__slug=self.kwargs['slug'],
            is_active=True
        )

    def perform_create(self, serializer):
        listing = get_object_or_404(Listing, slug=self.kwargs['slug'], seller=self.request.user)
        serializer.save(listing=listing)


class ListingOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Seller/Admin: edit or delete an offer"""
    serializer_class = ListingOfferSerializer
    permission_classes = [IsListingSellerOrAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ListingOffer.objects.none()
        return ListingOffer.objects.filter(listing__slug=self.kwargs['slug'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


# ── Admin ─────────────────────────────────────────────────────────────────────

class AdminListingListView(generics.ListAPIView):
    """Admin: all listings regardless of status"""
    serializer_class = ListingListSerializer
    permission_classes = [IsAdminOnly]
    queryset = Listing.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ListingFilter
    search_fields = ['title', 'city']


class AdminListingVerifyView(APIView):
    """Admin: toggle verified + auto-publish on verify"""
    permission_classes = [IsAdminOnly]

    def patch(self, request, slug):
        listing = get_object_or_404(Listing, slug=slug)
        listing.is_verified = not listing.is_verified
        # Auto publish when verified
        if listing.is_verified and listing.status == 'draft':
            listing.status = 'published'
        listing.save(update_fields=['is_verified', 'status'])
        return Response({'is_verified': listing.is_verified, 'status': listing.status})


class AdminListingFeatureView(APIView):
    """Admin: toggle featured"""
    permission_classes = [IsAdminOnly]

    def patch(self, request, slug):
        listing = get_object_or_404(Listing, slug=slug)
        listing.is_featured = not listing.is_featured
        listing.save(update_fields=['is_featured'])
        return Response({'is_featured': listing.is_featured})