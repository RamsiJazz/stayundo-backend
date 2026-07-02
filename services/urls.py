#services/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ServiceCategoryViewSet

router = DefaultRouter()
router.register('services', ServiceViewSet, basename='service')
router.register('service-categories', ServiceCategoryViewSet, basename='service-category')

urlpatterns = [
    path('', include(router.urls)),
]