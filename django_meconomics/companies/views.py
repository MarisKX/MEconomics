"""
Views for the companies API's
"""
# Django imports
from rest_framework import (
    viewsets,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Model imports
from companies.models import Company
# Serializers imports
from companies import serializers


class CompanyViewSet(viewsets.ModelViewSet):
    """View for manage companies API's"""
    serializer_class = serializers.CompanyDetailSerializer
    queryset = Company.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the srializer class for company"""
        if self.action == 'list':
            return serializers.CompanySerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new company"""
        serializer.save()
