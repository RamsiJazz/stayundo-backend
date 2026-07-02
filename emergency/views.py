from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly
from .models import EmergencyContact
from .serializers import EmergencyContactSerializer


class EmergencyContactViewSet(viewsets.ModelViewSet):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAdminOrReadOnly]