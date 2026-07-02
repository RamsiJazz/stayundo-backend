# content/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NewsPostViewSet,
    PublicHolidayViewSet,
    CityClimateViewSet,
    FAQViewSet,
    SupportTicketViewSet,
)

router = DefaultRouter()
router.register(r'news', NewsPostViewSet, basename='news')
router.register(r'holidays', PublicHolidayViewSet, basename='holiday')
router.register(r'climate', CityClimateViewSet, basename='climate')
router.register(r'faqs', FAQViewSet, basename='faq')
router.register(r'tickets', SupportTicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]