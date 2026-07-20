# applications/serializers.py
from rest_framework import serializers
from .models import HostelApplication


# ── Student: submit application ─────────────────────────────────
class HostelApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelApplication
        fields = [
            'id', 'full_name', 'age', 'gender',
            'id_proof', 'duration_months', 'preferred_room_type', 'message',
        ]
        read_only_fields = ['id']


    def validate(self, attrs):
        request = self.context['request']
        listing = self.context['listing']

        if listing.category.housing_type != 'hostel':
            raise serializers.ValidationError("Applications are only allowed for hostel listings.")
        if listing.status != 'published' or not listing.is_active:
            raise serializers.ValidationError("This listing is not currently accepting applications.")

        # Gender policy check
        pref = listing.gender_preference
        if pref != 'any' and attrs['gender'] != pref:
            raise serializers.ValidationError(
                {"gender": f"This hostel only accepts {pref} applicants."}
            )

        # Minimum stay check
        if attrs['duration_months'] < listing.min_stay_months:
            raise serializers.ValidationError(
                {"duration_months": f"Minimum stay for this hostel is {listing.min_stay_months} month(s)."}
            )

        # Duplicate pending application check
        if HostelApplication.objects.filter(
            listing=listing, applicant=request.user, status='pending'
        ).exists():
            raise serializers.ValidationError("You already have a pending application for this listing.")

        return attrs

    def create(self, validated_data):
        validated_data['applicant'] = self.context['request'].user
        validated_data['listing'] = self.context['listing']
        return super().create(validated_data)


# ── Read view: student sees own application, seller sees list ────
class HostelApplicationSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    applicant_name = serializers.CharField(source='applicant.name', read_only=True)
    applicant_email = serializers.CharField(source='applicant.email', read_only=True)

    class Meta:
        model = HostelApplication
        fields = [
            'id', 'listing', 'listing_title',
            'applicant', 'applicant_name', 'applicant_email',
            'full_name', 'age', 'gender', 'id_proof',
            'duration_months', 'preferred_room_type', 'message',
            'status', 'review_note', 'payment_details', 'admission_details',
            'reviewed_at', 'created_at', 'updated_at',
        ]
        read_only_fields = fields


# ── Seller: approve/reject + share details ────────────────────────
class HostelApplicationReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelApplication
        fields = ['status', 'review_note', 'payment_details', 'admission_details']

    def validate_status(self, value):
        if value not in ('approved', 'rejected'):
            raise serializers.ValidationError("Status must be 'approved' or 'rejected'.")
        return value
    

    def update(self, instance, validated_data):
        from django.utils import timezone
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.reviewed_at = timezone.now()
        instance.save()
        return instance