#listings.filters.py
import django_filters
from .models import Listing


class ListingFilter(django_filters.FilterSet):
    # Price
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    # Location
    city = django_filters.CharFilter(field_name="city", lookup_expr="iexact")
    state = django_filters.CharFilter(field_name="state", lookup_expr="iexact")

    # Category
    category = django_filters.UUIDFilter(field_name="category__id")  # fixed: UUID not Number

    # Rating
    min_rating = django_filters.NumberFilter(field_name="average_rating", lookup_expr="gte")

    # Stay
    gender_preference = django_filters.CharFilter(field_name="gender_preference", lookup_expr="iexact")
    food_available = django_filters.BooleanFilter(field_name="food_available")
    quality_grade = django_filters.CharFilter(field_name="quality_grade", lookup_expr="iexact")

    class Meta:
        model = Listing
        fields = [
            "city", "state",
            "status", "is_active", "is_featured", "is_verified",
            "gender_preference", "food_available", "quality_grade",
        ]
        # Removed: "country" — not a field on Listing model