#categories/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Housing Categories (Image 1)
    path('housing-categories/', views.HousingCategoryListView.as_view(), name='housing-category-list'),
    path('admin/housing-categories/', views.HousingCategoryAdminView.as_view(), name='housing-category-admin'),
    path('housing-categories/<slug:slug>/', views.HousingCategoryDetailView.as_view(), name='housing-category-detail'),

    # Expense Categories (Image 2)
    path('expense-categories/', views.ExpenseCategoryListView.as_view(), name='expense-category-list'),
    path('admin/expense-categories/', views.ExpenseCategoryAdminView.as_view(), name='expense-category-admin'),
    path('expense-categories/<slug:slug>/', views.ExpenseCategoryDetailView.as_view(), name='expense-category-detail'),

    
]