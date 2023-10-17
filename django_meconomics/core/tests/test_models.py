"""
Tests for Core models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import AppSettings
from datetime import date


class UserModelTests(TestCase):
    """Test models"""
    def test_create_user_with_email_successfull(self):
        """Test creating a user with an email is successfull."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'samplepas123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class AppSettingsModelTests(TestCase):

    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.app_settings = AppSettings(
            valid_from=date(1800, 1, 1),
            valid_till=date(1800, 1, 31),
            actions_per_day=5,
            vsaoi_dn=35,
            iin_rate=15,
            no_iin_level=50,
            uin_rate=20,
            enviroment_tax_base=0.01,
            btw=21,
            vsaoi_dd=9,
            base_cadastre_value=0.05,
        )
        self.app_settings.save()

    def test_app_settings_creation(self):
        """Test if an AppSettings instance can be created with valid fields."""
        self.app_settings.save()
        settings_number = self.app_settings.settings_number
        app_settings = AppSettings.objects.get(settings_number=settings_number)
        self.assertIsInstance(app_settings, AppSettings)

    def test_settings_number_generation(self):
        """Test that a new settings number is generated on save."""
        self.app_settings.save()
        self.assertIsNotNone(self.app_settings.settings_number)

    def test_previous_settings_invalidation(self):
        """Test that previous settings are invalid when saving new settings."""
        self.assertTrue(self.app_settings.valid)

        app_settings_new = AppSettings(
            valid_from=date(1800, 2, 1),
            valid_till=date(1800, 3, 31),
            actions_per_day=5,
            vsaoi_dn=35,
            iin_rate=15,
            no_iin_level=50,
            uin_rate=20,
            enviroment_tax_base=0.01,
            btw=21,
            vsaoi_dd=9,
            base_cadastre_value=0.05,
        )
        app_settings_new.save()

        settings_count = AppSettings.objects.all().count()
        print(settings_count)

        self.app_settings.refresh_from_db()
        self.assertFalse(self.app_settings.valid)
