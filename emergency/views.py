#emergency/views.py
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly
from .models import EmergencyContact
from .serializers import EmergencyContactSerializer


class EmergencyContactViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = EmergencyContact.objects.all()

        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            qs = qs.filter(is_active=True)

        return qs