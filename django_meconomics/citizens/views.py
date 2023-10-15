"""
Views for the citizens API's
"""
from rest_framework import (
    viewsets,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from citizens.models import (
    Citizen,
)
from citizens import serializers


class CitizenViewSet(viewsets.ModelViewSet):
    """View for manage citizens API's"""
    serializer_class = serializers.CitizenDetailSerializer
    queryset = Citizen.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the srializer class for citizen"""
        if self.action == 'list':
            return serializers.CitizenSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new citizen"""
        serializer.save()
