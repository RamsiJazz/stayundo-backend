#subscriptions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Plans
    path('plans/', views.SubscriptionPlanListView.as_view(), name='plan-list'),
    path('admin/plans/', views.SubscriptionPlanAdminView.as_view(), name='plan-admin'),
    path('admin/plans/<int:pk>/', views.SubscriptionPlanDetailView.as_view(), name='plan-detail'),

    # User subscriptions
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('my/', views.MySubscriptionsView.as_view(), name='my-subscriptions'),
    path('my/active/', views.MyActiveSubscriptionView.as_view(), name='my-active-subscription'),
    path('my/<int:id>/cancel/', views.CancelSubscriptionView.as_view(), name='subscription-cancel'),

    # Admin oversight
    path('admin/all/', views.AdminSubscriptionListView.as_view(), name='admin-subscription-list'),
]