# listings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ── Fixed/literal paths FIRST ──────────────────────────
    path('create/', views.ListingCreateView.as_view(), name='listing-create'),
    path('my-listings/', views.MyListingsView.as_view(), name='my-listings'),
    path('amenities/', views.AmenityListCreateView.as_view(), name='amenity-list'),

    # ── Admin (also literal, must come before slug) ────────
    path('admin/', views.AdminListingListView.as_view(), name='admin-listing-list'),
    path('admin/<slug:slug>/verify/', views.AdminListingVerifyView.as_view(), name='admin-listing-verify'),
    path('admin/<slug:slug>/feature/', views.AdminListingFeatureView.as_view(), name='admin-listing-feature'),

    # ── Public / Buyer ──────────────────────────────────────
    path('', views.ListingListView.as_view(), name='listing-list'),
    path('<slug:slug>/', views.ListingDetailView.as_view(), name='listing-detail'),
    path('<slug:slug>/specs/', views.ListingSpecListCreateView.as_view(), name='listing-spec-list'),
    path('<slug:slug>/offers/', views.ListingOfferListCreateView.as_view(), name='listing-offer-list'),

    # ── Seller (slug-based edit stays after fixed 'create/') ─
    path('<slug:slug>/edit/', views.ListingUpdateDeleteView.as_view(), name='listing-edit'),

    # ── Images ───────────────────────────────────────────────
    path('<slug:slug>/images/', views.ListingImageUploadView.as_view(), name='listing-image-upload'),
    path('<slug:slug>/images/<int:pk>/', views.ListingImageDeleteView.as_view(), name='listing-image-delete'),

    # ── Amenities (per-listing mapping) ─────────────────────
    path('<slug:slug>/amenities/', views.ListingAmenityAddView.as_view(), name='listing-amenity-add'),
    path('<slug:slug>/amenities/<int:pk>/', views.ListingAmenityRemoveView.as_view(), name='listing-amenity-remove'),

    # ── Specs & Offers detail (seller write) ────────────────
    path('<slug:slug>/specs/<int:pk>/', views.ListingSpecDetailView.as_view(), name='listing-spec-detail'),
    path('<slug:slug>/offers/<int:pk>/', views.ListingOfferDetailView.as_view(), name='listing-offer-detail'),
]