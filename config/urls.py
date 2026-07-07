"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Swagger schema setup
schema_view = get_schema_view(
   openapi.Info(
      title="StayUndo API",
      default_version='v1',
      description="API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

     # app APIs
    path('api/', include('users.urls')),
    # booking APIs
    path('api/booking/', include('booking.urls')),
    # categories APIs
    path('api/categories/', include('categories.urls')),
    # content APIs
    path('api/content/', include('content.urls')),
    # coupons APIs
    path('api/coupons/', include('coupons.urls')),
    # emergency APIs
    path('api/emergency/', include('emergency.urls')),
    # listings APIs
    path('api/listings/', include('listings.urls')),
    # products APIs
    path('api/products/', include('products.urls')),
    # services APIs
    path('api/services/', include('services.urls')),
    # subscriptions APIs
    path('api/subscriptions/', include('subscriptions.urls')),   
    # applications APIs
    path('api/applications/', include('applications.urls')),
     # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]
