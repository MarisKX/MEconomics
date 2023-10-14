# Django imports
from django.test import TestCase
from django.core.exceptions import ValidationError
# Other model imports
from companies.models import Company
from citizens.models import Citizen


class CompanyModelTests(TestCase):

    def setUp(self):
        # Create a Citizen
        self.citizen = Citizen(
            first_name="John",
            last_name="Doe",
            street_adress_1=123,
            street_adress_2="Apt 4B",
            city="New York",
            post_code="10001",
            country="USA",
        )
        self.citizen.save()

        # Create a Company with owner_pp set to Citizen
        self.company = Company(
            name="Example Company",
            established="2023-01-01",
            invoice_prefix="EX",
            owner_pp=self.citizen,  # Use the Citizen instance
            # Add other required fields here...
        )

    def test_company_creation(self):
        """Test if a Company instance can be created."""
        self.company.save()
        self.assertIsInstance(self.company, Company)

    def test_str_method(self):
        """Test the string representation of a Company."""
        self.company.save()
        self.assertEqual(str(self.company), "example_company")

    def test_get_display_name(self):
        """Test the get_display_name method."""
        self.company.save()
        self.assertEqual(self.company.get_display_name(), "Example Company")

    def test_registration_number_generation(self):
        """Test that a registration number is generated on save."""
        self.company.registration_number = None
        self.company.save()
        self.assertIsNotNone(self.company.registration_number)

    def test_employee_count_defaults_to_zero(self):
        """Test that the employee_count field defaults to zero."""
        self.company.save()
        self.assertEqual(self.company.employee_count, 0)

    def test_owner_pp_and_com_mutual_exclusivity(self):
        """Test that owner_pp and owner_com can't both be set."""
        another_company = Company(
            name="Another Company",
            established="2023-01-02",
            invoice_prefix="AC",
            owner_pp=self.citizen
        )
        another_company.save()
        self.company.owner_com = another_company
        with self.assertRaises(ValidationError):
            self.company.save()