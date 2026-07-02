#products/views.py
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, filters
from .models import Product, ProductCategory
from .serializers import (
    ProductCategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductContactSerializer, ProductSerializer,
)
from .permissions import IsOwnerOrAdmin, IsAdminOrReadOnly


# --- Categories ---

class ProductCategoryListView(generics.ListAPIView):
    """Public: list product categories (Furniture, Electronics, etc.)"""
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductCategoryAdminView(generics.ListCreateAPIView):
    """Admin only: create/manage product categories"""
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


# --- Products: public browsing ---

class ProductListView(generics.ListAPIView):
    """Public: browse used products. No contact info here."""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        qs = Product.objects.filter(is_available=True)
        category = self.request.query_params.get('category')
        condition = self.request.query_params.get('condition')
        location = self.request.query_params.get('location')
        if category:
            qs = qs.filter(category__slug=category)
        if condition:
            qs = qs.filter(condition=condition)
        if location:
            qs = qs.filter(location__icontains=location)
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    """Public: full product details, no contact info yet."""
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)


class ProductContactView(generics.RetrieveAPIView):
    """Authenticated buyers: reveal owner's contact info on demand."""
    serializer_class = ProductContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)


# --- Products: owner/admin management ---

class ProductCreateView(generics.CreateAPIView):
    """Authenticated sellers/admins can post a used product."""
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyProductsView(generics.ListAPIView):
    """Owner: list their own posted products."""
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)


class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Owner or admin: edit/delete; e.g. PATCH is_available=False to mark sold."""
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(owner=user)