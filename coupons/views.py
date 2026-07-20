#coupons/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .models import Coupon, CouponUsage
from .serializers import (
    CouponSerializer, CouponPublicSerializer,
    CouponValidateSerializer, CouponUsageSerializer,
)
from .permissions import IsAdminOnly, IsAdminOrAuthenticatedReadOnly


# ── Admin ─────────────────────────────────────────────────────────────────────

class CouponListCreateView(generics.ListCreateAPIView):
    """Admin: list all coupons / create new coupon"""
    serializer_class = CouponSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Coupon.objects.all()

        now = timezone.now()
        return Coupon.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CouponDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: get, update, delete a coupon"""
    serializer_class = CouponSerializer
    permission_classes = [IsAdminOnly]
    queryset = Coupon.objects.all()
    lookup_field = 'id'


class CouponUsageListView(generics.ListAPIView):
    """Admin: see all usage history of a coupon"""
    serializer_class = CouponUsageSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CouponUsage.objects.none()
        return CouponUsage.objects.filter(coupon__id=self.kwargs['id'])


# ── Buyer/Seller ──────────────────────────────────────────────────────────────

class CouponValidateView(APIView):
    """
    Buyer: validate a coupon before booking.
    POST { "code": "SAVE20", "listing_id": "<uuid>", "amount": 5000 }
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=CouponValidateSerializer)
    def post(self, request):
        serializer = CouponValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        listing_id = serializer.validated_data.get('listing_id')
        amount = serializer.validated_data.get('amount', 0)

        coupon = get_object_or_404(Coupon, code__iexact=code)

        # 1. Check coupon validity
        if not coupon.is_valid():
            return Response(
                {"detail": "Coupon is expired or inactive."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Check listing scope
        if listing_id and coupon.category == 'specific':
            if not coupon.listings.filter(id=listing_id).exists():
                return Response(
                    {"detail": "Coupon is not valid for this listing."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 3. Check per-user limit
        user_usage_count = CouponUsage.objects.filter(
            coupon=coupon, user=request.user
        ).count()

        if user_usage_count >= coupon.per_user_limit:
            return Response(
                {"detail": "You have already used this coupon."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Calculate discount
        discount = coupon.calculate_discount(amount) if amount else coupon.discount_value

        return Response({
            "code": coupon.code,
            "description": coupon.description,
            "discount_type": coupon.discount_type,
            "discount_value": coupon.discount_value,
            "calculated_discount": discount,
            "message": "Coupon is valid.",
        }, status=status.HTTP_200_OK)


class MyUsedCouponsView(generics.ListAPIView):
    """Buyer: see own coupon usage history"""
    serializer_class = CouponUsageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CouponUsage.objects.none()
        return CouponUsage.objects.filter(user=self.request.user)