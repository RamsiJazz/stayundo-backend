# categories/views.py
from rest_framework import generics
from .models import HousingCategory, ExpenseCategory
from .serializers import HousingCategorySerializer, ExpenseCategorySerializer
from .permissions import IsAdminOrReadOnly


class HousingCategoryListCreateView(generics.ListCreateAPIView):
    """
    GET: public — active categories only for regular users, all for admins
    POST: admin only
    """
    serializer_class = HousingCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return HousingCategory.objects.all()
        return HousingCategory.objects.filter(is_active=True)


class HousingCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HousingCategory.objects.all()
    serializer_class = HousingCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class ExpenseCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return ExpenseCategory.objects.all()
        return ExpenseCategory.objects.filter(is_active=True)


class ExpenseCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'