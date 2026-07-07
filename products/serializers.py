#products/serializers.py
from rest_framework import serializers
from users.models import User
from .models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id']


# --- Browse view: no contact info ---
class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'title', 'image', 'price',
            'condition', 'location', 'is_available', 'created_at',
        ]


# --- Detail view: full info, still no contact info ---
class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'description', 'title', 'image', 'price',
            'condition', 'location', 'is_available', 'created_at',
        ]


# --- Contact reveal: only when buyer explicitly requests it ---
class OwnerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone']  # matches users.models.User


class ProductContactSerializer(serializers.ModelSerializer):
    owner = OwnerContactSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'owner']


# --- Owner/Admin: create & manage ---
class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'title', 'description', 'image',
            'price', 'condition', 'location', 'owner', 'is_available', 'created_at',
        ]
        read_only_fields = ['id', 'owner', 'created_at']