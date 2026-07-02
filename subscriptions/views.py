#subscriptions/views.py
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import SubscriptionPlan, UserSubscription
from .serializers import (
    SubscriptionPlanSerializer, UserSubscriptionSerializer, SubscribeSerializer,
)
from .permissions import IsAdminOrReadOnly


# --- Plans ---

class SubscriptionPlanListView(generics.ListAPIView):
    """Public: list active plans, optionally filtered by plan_for=buyer/seller"""
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = SubscriptionPlan.objects.filter(is_active=True)
        plan_for = self.request.query_params.get('plan_for')
        if plan_for:
            qs = qs.filter(plan_for=plan_for)
        return qs


class SubscriptionPlanAdminView(generics.ListCreateAPIView):
    """Admin only: create/manage plans"""
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminOrReadOnly]


class SubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminOrReadOnly]


# --- User subscriptions ---

class SubscribeView(generics.CreateAPIView):
    """Authenticated user: subscribe to a plan (buyer or seller)"""
    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        return Response(
            UserSubscriptionSerializer(subscription).data,
            status=status.HTTP_201_CREATED,
        )


class MySubscriptionsView(generics.ListAPIView):
    """Authenticated user: see their subscription history"""
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user)


class MyActiveSubscriptionView(APIView):
    """Authenticated user: check current active subscription status"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sub = UserSubscription.objects.filter(
            user=request.user, status='active', end_date__gte=timezone.now()
        ).order_by('-end_date').first()

        if not sub:
            return Response({"has_active_subscription": False})

        return Response({
            "has_active_subscription": True,
            "subscription": UserSubscriptionSerializer(sub).data,
        })


class CancelSubscriptionView(APIView):
    """Authenticated user: cancel their own active subscription"""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, id):
        try:
            sub = UserSubscription.objects.get(id=id, user=request.user, status='active')
        except UserSubscription.DoesNotExist:
            return Response(
                {"detail": "Active subscription not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        sub.status = 'cancelled'
        sub.save(update_fields=['status'])
        return Response({"detail": "Subscription cancelled."})


# --- Admin oversight ---

class AdminSubscriptionListView(generics.ListAPIView):
    """Admin: view all subscriptions across all users"""
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = UserSubscription.objects.all()