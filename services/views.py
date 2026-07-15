#services/views.py
from rest_framework import viewsets, filters
from .models import Service, ServiceCategory
from .serializers import ServiceSerializer, ServiceCategorySerializer
from .permissions import IsAdminOrReadOnly


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ServiceCategory.objects.none()
        return ServiceCategory.objects.filter(is_active=True)


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'category__name']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Service.objects.none()
        qs = Service.objects.select_related(
            'category',
            'mess_detail',
            'transport_detail',
            'hospital_detail',
            'attraction_detail',
            'security_detail',
            'education_detail',
        )
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)
        # ?type=mess  ?type=hospital  ?type=taxi etc.
        service_type = self.request.query_params.get('type')
        city = self.request.query_params.get('city')

        if service_type:
            qs = qs.filter(category__service_type=service_type)
        if city:
            qs = qs.filter(city__icontains=city)
        return qs