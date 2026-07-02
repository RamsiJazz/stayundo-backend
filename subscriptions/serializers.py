#subscriptions/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import SubscriptionPlan, UserSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'plan_for', 'duration_days', 'price',
            'is_free_trial', 'is_active', 'description',
        ]
        read_only_fields = ['id']


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = UserSubscription
        fields = [
            'id', 'plan', 'start_date', 'end_date', 'status',
            'amount_paid', 'payment_reference', 'used_free_trial', 'created_at',
        ]
        read_only_fields = fields


class SubscribeSerializer(serializers.Serializer):
    """Used to create a new subscription for the logged-in user."""
    plan_id = serializers.IntegerField()
    payment_reference = serializers.CharField(required=False, allow_blank=True)

    def validate_plan_id(self, value):
        try:
            plan = SubscriptionPlan.objects.get(id=value, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive plan.")
        self.plan = plan
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        plan = self.plan

        # Enforce seller free trial — only usable once per user
        amount_paid = plan.price
        used_free_trial = False

        if plan.is_free_trial:
            already_used = UserSubscription.objects.filter(
                user=user, plan__is_free_trial=True
            ).exists()
            if already_used:
                raise serializers.ValidationError(
                    "Free trial has already been used."
                )
            amount_paid = 0
            used_free_trial = True

        subscription = UserSubscription.objects.create(
            user=user,
            plan=plan,
            start_date=timezone.now(),
            amount_paid=amount_paid,
            payment_reference=validated_data.get('payment_reference', ''),
            used_free_trial=used_free_trial,
            status='active',
        )
        return subscription