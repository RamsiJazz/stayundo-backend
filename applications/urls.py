# applications/urls.py
from django.urls import path
from .views import (
    HostelApplicationCreateView, MyApplicationsView, MyApplicationDetailView,
    ListingApplicationListView, ApplicationReviewView,
)

urlpatterns = [
    # Student
    path('apply/', HostelApplicationCreateView.as_view(), name='hostel-apply'),
    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),
    path('my-applications/<uuid:pk>/', MyApplicationDetailView.as_view(), name='my-application-detail'),

    # Seller
    path('listings/<slug:slug>/applications/', ListingApplicationListView.as_view(), name='listing-applications'),
    path('<uuid:pk>/review/', ApplicationReviewView.as_view(), name='application-review'),
]