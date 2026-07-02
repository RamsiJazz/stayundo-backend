#booking.urls.py
from django.urls import path
from . import views

urlpatterns = [

    # ── Tenant ───────────────────────────────────────────────
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/my/', views.MyBookingsView.as_view(), name='my-bookings'),
    path('bookings/my/<uuid:id>/', views.MyBookingDetailView.as_view(), name='my-booking-detail'),
    path('bookings/my/<uuid:id>/cancel/', views.BookingCancelView.as_view(), name='booking-cancel'),

    # ── Seller ───────────────────────────────────────────────
    path('bookings/seller/', views.SellerBookingsView.as_view(), name='seller-bookings'),
    path('bookings/seller/<uuid:id>/', views.SellerBookingDetailView.as_view(), name='seller-booking-detail'),
    path('bookings/seller/<uuid:id>/status/', views.SellerBookingStatusView.as_view(), name='seller-booking-status'),
    path('bookings/seller/<uuid:id>/note/', views.SellerBookingNoteView.as_view(), name='seller-booking-note'),

    # ── Admin ────────────────────────────────────────────────
    path('admin/bookings/', views.AdminBookingListView.as_view(), name='admin-booking-list'),
    path('admin/bookings/<uuid:id>/', views.AdminBookingDetailView.as_view(), name='admin-booking-detail'),
    path('admin/bookings/<uuid:id>/status/', views.AdminBookingStatusView.as_view(), name='admin-booking-status'),
]