# categories/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('housing-categories/', views.HousingCategoryListCreateView.as_view(), name='housing-category-list-create'),
    path('housing-categories/<slug:slug>/', views.HousingCategoryDetailView.as_view(), name='housing-category-detail'),

    path('expense-categories/', views.ExpenseCategoryListCreateView.as_view(), name='expense-category-list-create'),
    path('expense-categories/<slug:slug>/', views.ExpenseCategoryDetailView.as_view(), name='expense-category-detail'),
]