#categories/views.py
from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from .models import HousingCategory, ExpenseCategory
from .serializers import HousingCategorySerializer, ExpenseCategorySerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

# --- Housing Categories  ---

class HousingCategoryListView(generics.ListAPIView):
    """Public: List all active housing categories"""
    queryset = HousingCategory.objects.filter(is_active=True)
    serializer_class = HousingCategorySerializer
    permission_classes = [permissions.AllowAny]

class HousingCategoryAdminView(generics.ListCreateAPIView):
    """Admin only: Create/manage housing categories"""
    queryset = HousingCategory.objects.all()
    serializer_class = HousingCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class HousingCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HousingCategory.objects.all()
    serializer_class = HousingCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'

# --- Expense Categories ---

class ExpenseCategoryListView(generics.ListAPIView):
    """Public: Browse all expense categories"""
    queryset = ExpenseCategory.objects.filter(is_active=True)
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.AllowAny]
   

class ExpenseCategoryAdminView(generics.ListCreateAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ExpenseCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'