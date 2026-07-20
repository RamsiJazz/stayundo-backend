#content/serializers.py

# content/serializers.py
from rest_framework import serializers
from users.models import User
from .models import NewsPost, PublicHoliday, CityClimate, FAQ, SupportTicket


class NewsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPost
        fields = [
            'id', 'title', 'category', 'summary', 'image',
            'source_link', 'city', 'is_active',
            'published_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PublicHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicHoliday
        fields = [
            'id', 'name', 'date', 'description',
            'is_national', 'state',
        ]
        read_only_fields = ['id']


class CityClimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityClimate
        fields = [
            'id', 'city', 'summary', 'best_time_to_visit',
            'banner_image', 'weather_api_city_key',
        ]
        read_only_fields = ['id']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'order', 'is_active']
        read_only_fields = ['id']


class SupportTicketUserSerializer(serializers.ModelSerializer):
    """Minimal nested representation of the ticket owner."""
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']


class SupportTicketSerializer(serializers.ModelSerializer):
    user = SupportTicketUserSerializer(read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            'id', 'user', 'subject', 'message',
            'status', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Force the ticket to belong to the requesting user,
        # never trust a client-supplied user id.
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)


class SupportTicketStatusUpdateSerializer(serializers.ModelSerializer):
    """Used only by admins to change ticket status."""
    class Meta:
        model = SupportTicket
        fields = ['id', 'status']
        read_only_fields = ['id']