#coupons/serializers.py
from rest_framework import serializers
from .models import Coupon, CouponUsage


class CouponSerializer(serializers.ModelSerializer):
    is_valid_now = serializers.SerializerMethodField()
    remaining_uses = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'description',
            'discount_type', 'discount_value', 'max_discount_cap',
            'category', 'listings',
            'start_date', 'end_date',
            'usage_limit', 'used_count', 'per_user_limit',
            'is_active',
            'created_by_name', 'created_at',
            'is_valid_now', 'remaining_uses',
        ]
        read_only_fields = ['id', 'used_count', 'created_at', 'created_by_name']

    def get_is_valid_now(self, obj):
        return obj.is_valid()

    def get_remaining_uses(self, obj):
        return obj.usage_limit - obj.used_count


class CouponPublicSerializer(serializers.ModelSerializer):
    """Minimal — shown to tenant after validation"""
    class Meta:
        model = Coupon
        fields = ['code', 'description', 'discount_type', 'discount_value', 'max_discount_cap']


class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)
    listing_id = serializers.UUIDField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)  # to calc discount


class CouponUsageSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    coupon_code = serializers.CharField(source='coupon.code', read_only=True)

    class Meta:
        model = CouponUsage
        fields = ['id', 'coupon_code', 'user_name', 'used_at', 'booking_id']