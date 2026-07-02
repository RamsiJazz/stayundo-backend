#coupons/urls.py
from django.urls import path
from . import views
from coupons.views import CouponListCreateView
urlpatterns = [

    # ── Admin ────────────────────────────────────────────────
    path('coupons/', views.CouponListCreateView.as_view(), name='coupon-list-create'),
    path('coupons/<uuid:id>/', views.CouponDetailView.as_view(), name='coupon-detail'),
    path('coupons/<uuid:id>/usages/', views.CouponUsageListView.as_view(), name='coupon-usages'),

    # ── Buyer ────────────────────────────────────────────────
    path('coupons/validate/', views.CouponValidateView.as_view(), name='coupon-validate'),
    path('coupons/my-usage/', views.MyUsedCouponsView.as_view(), name='my-coupon-usage'),
]