#products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.ProductCategoryListView.as_view(), name='product-category-list'),
    path('admin/categories/', views.ProductCategoryAdminView.as_view(), name='product-category-admin'),
    path('categories/<slug:slug>/', views.ProductCategoryDetailView.as_view(), name='product-category-detail'),

    # Public browsing
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:id>/contact/', views.ProductContactView.as_view(), name='product-contact'),

    # Owner/admin management
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('my/', views.MyProductsView.as_view(), name='my-products'),
    path('my/<int:id>/', views.ProductUpdateView.as_view(), name='product-update'),
]