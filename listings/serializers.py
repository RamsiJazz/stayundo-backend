#listings/serializers.py
from rest_framework import serializers
from .models import (
    Listing, ListingImage, ListingAmenity,
    ListingAmenityMapping, ListingSpecification, ListingOffer
)


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'display_order']


class ListingAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingAmenity
        fields = ['id', 'name', 'icon']


class ListingAmenityMappingSerializer(serializers.ModelSerializer):
    amenity = ListingAmenitySerializer(read_only=True)
    amenity_id = serializers.PrimaryKeyRelatedField(
        queryset=ListingAmenity.objects.all(), source='amenity', write_only=True
    )

    class Meta:
        model = ListingAmenityMapping
        fields = ['id', 'amenity', 'amenity_id']


class ListingSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingSpecification
        fields = ['id', 'key', 'value']


class ListingOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingOffer
        fields = ['id', 'title', 'description', 'discount_value', 'valid_until', 'is_active']


# ── Buyer/Public: minimal card ────────────────────────────────────────────────
class ListingListSerializer(serializers.ModelSerializer):
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    active_offers_count = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'slug', 'cover_image',
            'city', 'state', 'address',
            'price', 'discount_price', 'effective_price',
            'category_name', 'quality_grade',
            'average_rating', 'total_reviews',
            'is_featured', 'is_verified',
            'active_offers_count',
        ]

    def get_active_offers_count(self, obj):
        return obj.offers.filter(is_active=True).count()


# ── Buyer/Public: full detail ─────────────────────────────────────────────────
class ListingDetailSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    amenity_mappings = ListingAmenityMappingSerializer(many=True, read_only=True)
    specifications = ListingSpecificationSerializer(many=True, read_only=True)
    offers = ListingOfferSerializer(many=True, read_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'seller_name', 'category_name', 'quality_grade', 'status',

            'cover_image', 'images',

            'address', 'city', 'district','state', 'google_map_link', 'latitude', 'longitude',

            'phone', 'website',

            'price', 'discount_price', 'effective_price',
            'security_deposit', 'advance_deposit',

            'food_available', 'food_description', 'food_price_per_month',

            'security_available', 'security_type', 'security_details',
            
            'stay_rules', 'gender_preference', 'min_stay_months',

            'amenity_mappings', 'specifications', 'offers',

            'is_featured', 'is_verified', 'is_active',
            'average_rating', 'total_reviews', 'total_views',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'seller_name', 'average_rating',
            'total_reviews', 'total_views', 'created_at', 'updated_at'
        ]


# ── Seller: create / update ───────────────────────────────────────────────────
class ListingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'category', 'title', 'slug', 'description', 'short_description',
            'cover_image', 'quality_grade', 'status',

            'address', 'city', 'district','state', 'google_map_link', 'latitude', 'longitude',

            'phone', 'website',

            'price', 'discount_price', 'security_deposit', 'advance_deposit',

            'food_available', 'food_description', 'food_price_per_month',
            'security_available',
            'security_type', 'security_details',

            'stay_rules', 'gender_preference', 'min_stay_months',

            'is_active',
        ]

    def validate(self, attrs):
        # Seller cannot self-publish — admin must verify first
        if attrs.get('status') == 'published':
            user = self.context['request'].user
            if not user.is_staff:
                raise serializers.ValidationError(
                    {"status": "Sellers cannot publish directly. Submit for admin review."}
                )
        return attrs