"""
Tests for Citizen models.
"""
from django.test import TestCase
from citizens.models import Citizen


class CitizenModelTests(TestCase):

    def setUp(self):
        self.citizen = Citizen(
            first_name="John",
            last_name="Doe",
            street_adress_1=123,
            street_adress_2="Apt 4B",
            city="New York",
            post_code="10001",
            country="USA",
        )

    def test_citizen_creation(self):
        """Test if a Citizen instance can be created."""
        self.citizen.save()
        self.assertIsInstance(self.citizen, Citizen)

    def test_str_method(self):
        """Test the string representation of a Citizen."""
        self.citizen.save()
        self.assertEqual(str(self.citizen), "john_doe")

    def test_get_full_name(self):
        """Test the get_full_name method."""
        self.citizen.save()
        self.assertEqual(self.citizen.get_full_name(), "John Doe")

    def test_get_house_number(self):
        """Test the get_house_number method."""
        self.citizen.save()
        self.assertEqual(self.citizen.get_house_number(), 123)

    def test_bsn_number_generation(self):
        """Test that a unique BSN number is generated on save."""
        # Save multiple Citizen instances and check if BSN numbers are unique.
        citizen1 = Citizen(
            first_name="Alice",
            last_name="Smith",
        )
        citizen1.save()
        citizen2 = Citizen(
            first_name="Bob",
            last_name="Johnson",
        )
        citizen2.save()
        self.assertNotEqual(citizen1.bsn_number, citizen2.bsn_number)

    def test_save_method(self):
        """Test the overridden save method."""
        self.citizen.first_name = "John"
        self.citizen.last_name = "Doe"
        self.citizen.save()
        self.assertEqual(self.citizen.first_name_low, "john")
        self.assertEqual(self.citizen.last_name_low, "doe")
        self.assertEqual(self.citizen.name, "john_doe")

    def test_save_method_bsn_number(self):
        """Test that BSN number is generated if it's not provided."""
        self.citizen.bsn_number = None
        self.citizen.save()
        self.assertIsInstance(self.citizen.bsn_number, int)
