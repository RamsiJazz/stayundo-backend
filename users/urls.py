#users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,ProfileView,WishlistViewSet,ReviewViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path("profile/", ProfileView.as_view(), name="profile"),
]
