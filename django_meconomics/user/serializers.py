"""
Serializers for the user API View
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from core.models import AppSettings


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
                }
            }

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorizaion')
        attrs['user'] = user
        return attrs


class AppSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for listing App Settings.
    """
    class Meta:
        model = AppSettings
        fields = [
            'id',
            'settings_number',
            'valid_from',
            'valid_till',
            'actions_per_day',
            'valid',
        ]

    def create(self, validated_data):
        """Create and return a new citizen"""
        return AppSettings.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return a citizen"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AppSettingsDetailSerializer(AppSettingsSerializer):
    """
    Serializer for displaying detailed information
    about a App Settings.
    """
    class Meta(AppSettingsSerializer.Meta):
        fields = AppSettingsSerializer.Meta.fields + [
            'vsaoi_dn',
            'iin_rate',
            'no_iin_level',
            'uin_rate',
            'enviroment_tax_base',
            'btw',
            'vsaoi_dd',
            'base_cadastre_value',
        ]
