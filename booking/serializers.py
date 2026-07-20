#booking.serializers.py
from rest_framework import serializers
from .models import Booking, BookingStatusLog
from listings.models import Listing
from coupons.models import Coupon


class BookingStatusLogSerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(source='changed_by.name', read_only=True)

    class Meta:
        model = BookingStatusLog
        fields = ['id', 'old_status', 'new_status', 'note', 'changed_by_name', 'changed_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    """Used when tenant submits a booking"""
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Booking
        fields = [
            'listing', 'move_in_date', 'move_out_date',
            'duration_months', 'food_charges',
            'tenant_note', 'coupon_code',
        ]

    def validate(self, attrs):
        listing = attrs['listing']
        move_in = attrs['move_in_date']

        # Check listing is published
        if not listing.is_active or listing.status != 'published':
            raise serializers.ValidationError("This listing is not available.")

        # Check move_in not in past
        from django.utils import timezone
        if move_in < timezone.now().date():
            raise serializers.ValidationError("Move-in date cannot be in the past.")

        return attrs

    def create(self, validated_data):
        listing = validated_data['listing']
        coupon_code = validated_data.pop('coupon_code', '')
        food_charges = validated_data.get('food_charges', 0)

        # Price snapshot from listing
        rent = listing.discount_price or listing.price
        security = listing.security_deposit
        advance = listing.advance_deposit

        # Coupon discount
        discount = 0
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid():
                    discount = coupon.discount_value
            except Coupon.DoesNotExist:
                pass

        total = rent + security + advance + food_charges - discount

        return Booking.objects.create(
            **validated_data,
            coupon_code=coupon_code,
            rent_amount=rent,
            security_deposit=security,
            advance_deposit=advance,
            discount_amount=discount,
            total_amount=total,
            tenant=self.context['request'].user,
        )


class BookingListSerializer(serializers.ModelSerializer):
    """Minimal — for listing booking cards"""
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    listing_city = serializers.CharField(source='listing.city', read_only=True)
    listing_cover = serializers.URLField(source='listing.cover_image', read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'listing_title', 'listing_city', 'listing_cover',
            'tenant_name', 'move_in_date', 'duration_months',
            'total_amount', 'status', 'payment_status', 'created_at',
        ]


class BookingDetailSerializer(serializers.ModelSerializer):
    """Full detail"""
    status_logs = BookingStatusLogSerializer(many=True, read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    listing_slug = serializers.CharField(source='listing.slug', read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'listing_title', 'listing_slug',
            'tenant_name', 'tenant_email',

            'move_in_date', 'move_out_date', 'duration_months',

            'rent_amount', 'security_deposit', 'advance_deposit',
            'food_charges', 'discount_amount', 'total_amount',
            'coupon_code',

            'status', 'payment_status',
            'tenant_note', 'seller_note',

            'status_logs',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'rent_amount', 'security_deposit', 'advance_deposit',
            'discount_amount', 'total_amount', 'created_at', 'updated_at'
        ]


class BookingStatusUpdateSerializer(serializers.Serializer):
    """For seller/admin to change booking status"""
    status = serializers.ChoiceField(choices=Booking.STATUS_CHOICES)
    note = serializers.CharField(required=False, allow_blank=True)


class BookingSellerNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['seller_note']