from rest_framework import serializers
from .models import Service, ServiceCategory, MessRestaurantDetail, TransportDetail, HospitalDetail, AttractionDetail, SecurityDetail, EducationDetail


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

class SecurityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityDetail
        exclude = ['service']


class EducationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationDetail
        exclude = ['service']

DETAIL_CONFIG = {
    'mess_detail': (MessRestaurantDetail, MessRestaurantDetailSerializer),
    'transport_detail': (TransportDetail, TransportDetailSerializer),
    'hospital_detail': (HospitalDetail, HospitalDetailSerializer),
    'attraction_detail': (AttractionDetail, AttractionDetailSerializer),
    'security_detail': (SecurityDetail, SecurityDetailSerializer),
    'education_detail': (EducationDetail, EducationDetailSerializer),
}


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    service_type = serializers.CharField(source='category.service_type', read_only=True)

    # Only one will be non-null depending on the service type
    mess_detail = MessRestaurantDetailSerializer(read_only=True)
    transport_detail = TransportDetailSerializer(read_only=True)
    hospital_detail = HospitalDetailSerializer(read_only=True)
    attraction_detail = AttractionDetailSerializer(read_only=True)
    security_detail = SecurityDetailSerializer(required=False, allow_null=True)
    education_detail = EducationDetailSerializer(required=False, allow_null=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'category', 'category_name', 'service_type',
            'phone', 'maps_link', 'city', 'is_verified', 'is_active', 'created_at',
            'mess_detail', 'transport_detail', 'hospital_detail', 'attraction_detail',
            'security_detail', 'education_detail',
        ]
        read_only_fields = ['created_at']
def validate(self, attrs):
    # Guard against sending more than one detail type at once — the
    # models are 1:1 with Service, so only one should ever apply.
    detail_keys_present = [k for k in DETAIL_CONFIG if k in self.initial_data]
    if len(detail_keys_present) > 1:
        raise serializers.ValidationError(
            f"Only one detail type is allowed per service, got: {detail_keys_present}"
        )
    category = attrs.get('category') or getattr(self.instance, 'category', None)
    if detail_keys_present and category:
        expected_key = f"{category.service_type}_detail"
        if detail_keys_present[0] != expected_key and expected_key in DETAIL_CONFIG:
            raise serializers.ValidationError(
                f"'{detail_keys_present[0]}' doesn't match category service_type "
                f"'{category.service_type}' (expected '{expected_key}')"
            )
    return attrs

def _pop_detail_data(self, validated_data):
    """Remove and return whichever single detail payload was sent, if any."""
    for key in DETAIL_CONFIG:
        if key in validated_data:
            return key, validated_data.pop(key)
    return None, None

def create(self, validated_data):
    detail_key, detail_data = self._pop_detail_data(validated_data)
    service = Service.objects.create(**validated_data)

    if detail_key and detail_data is not None:
        model_cls, _ = DETAIL_CONFIG[detail_key]
        model_cls.objects.create(service=service, **detail_data)

    return service

def update(self, instance, validated_data):
    detail_key, detail_data = self._pop_detail_data(validated_data)

    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()

    if detail_key:
        model_cls, _ = DETAIL_CONFIG[detail_key]
        if detail_data is None:
            # allow clearing the detail record explicitly with `"mess_detail": null`
            model_cls.objects.filter(service=instance).delete()
        else:
            model_cls.objects.update_or_create(
                service=instance, defaults=detail_data
            )

    return instance


