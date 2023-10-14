"""
Serializers for the citizens API View
"""
# DRF imports
from rest_framework import serializers
# Custom imports
from citizens.models import Citizen


class CitizenSerializer(serializers.ModelSerializer):
    """Serializer for the citizen object"""

    class Meta:
        model = Citizen
        fields = [
            'id',
            'first_name',
            'last_name',
            'bsn_number',
            'street_adress_1',
            'street_adress_2',
            'city',
            'post_code',
            'country',
            ]

    def create(self, validated_data):
        """Create and return a new citizen"""
        return Citizen.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return a citizen"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CitizenDetailSerializer(CitizenSerializer):
    """Serializer for recipe detail view"""

    class Meta(CitizenSerializer.Meta):
        fields = CitizenSerializer.Meta.fields + [
            'name',
            'first_name_low',
            'last_name_low',
            ]
