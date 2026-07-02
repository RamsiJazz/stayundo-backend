from rest_framework import serializers
from .models import Service, ServiceCategory, MessRestaurantDetail, TransportDetail, HospitalDetail, AttractionDetail


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'service_type', 'icon', 'is_active']


class MessRestaurantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessRestaurantDetail
        exclude = ['service']


class TransportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportDetail
        exclude = ['service']


class HospitalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalDetail
        exclude = ['service']

class AttractionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttractionDetail
        exclude = ['service']


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    service_type = serializers.CharField(source='category.service_type', read_only=True)

    # Only one will be non-null depending on the service type
    mess_detail = MessRestaurantDetailSerializer(read_only=True)
    transport_detail = TransportDetailSerializer(read_only=True)
    hospital_detail = HospitalDetailSerializer(read_only=True)
    attraction_detail = AttractionDetailSerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'category', 'category_name', 'service_type',
            'phone', 'maps_link', 'city', 'is_verified', 'is_active', 'created_at',
            'mess_detail', 'transport_detail', 'hospital_detail', 'attraction_detail',
        ]
        read_only_fields = ['created_at']


