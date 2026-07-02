#listings/urls.py
from django.urls import path
from . import views

urlpatterns = [

    # ── Public / Buyer ───────────────────────────────────────
    path('listings/', views.ListingListView.as_view(), name='listing-list'),
    path('listings/<slug:slug>/', views.ListingDetailView.as_view(), name='listing-detail'),
    path('listings/<slug:slug>/specs/', views.ListingSpecListCreateView.as_view(), name='listing-spec-list'),
    path('listings/<slug:slug>/offers/', views.ListingOfferListCreateView.as_view(), name='listing-offer-list'),

    # ── Seller ───────────────────────────────────────────────
    path('listings/create/', views.ListingCreateView.as_view(), name='listing-create'),
    path('listings/<slug:slug>/edit/', views.ListingUpdateDeleteView.as_view(), name='listing-edit'),
    path('my-listings/', views.MyListingsView.as_view(), name='my-listings'),

    # ── Images ──────────────────────────────────────────────
    path('listings/<slug:slug>/images/', views.ListingImageUploadView.as_view(), name='listing-image-upload'),
    path('listings/<slug:slug>/images/<int:pk>/', views.ListingImageDeleteView.as_view(), name='listing-image-delete'),

    # ── Amenities ────────────────────────────────────────────
    path('amenities/', views.AmenityListCreateView.as_view(), name='amenity-list'),
    path('listings/<slug:slug>/amenities/', views.ListingAmenityAddView.as_view(), name='listing-amenity-add'),
    path('listings/<slug:slug>/amenities/<int:pk>/', views.ListingAmenityRemoveView.as_view(), name='listing-amenity-remove'),

    # ── Specs & Offers (seller write) ────────────────────────
    path('listings/<slug:slug>/specs/<int:pk>/', views.ListingSpecDetailView.as_view(), name='listing-spec-detail'),
    path('listings/<slug:slug>/offers/<int:pk>/', views.ListingOfferDetailView.as_view(), name='listing-offer-detail'),

    # ── Admin ─────────────────────────────────────────────────
    path('admin/listings/', views.AdminListingListView.as_view(), name='admin-listing-list'),
    path('admin/listings/<slug:slug>/verify/', views.AdminListingVerifyView.as_view(), name='admin-listing-verify'),
    path('admin/listings/<slug:slug>/feature/', views.AdminListingFeatureView.as_view(), name='admin-listing-feature'),
]