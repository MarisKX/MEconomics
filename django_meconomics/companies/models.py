# Django imports
from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Sum
# Other model imports
from citizens.models import Citizen
from core.models import AppSettings
# Custom imports
from core.custom_functions.letter_to_number import letter_to_number
from core.custom_functions.remove_accents import remove_accents


class Company(models.Model):
    class Meta:
        verbose_name_plural = 'Companies'
    owner_type_choices = [
        ('0', 'Private'),
        ('1', 'Company'),
        ('2', 'Government Institution'),
    ]
    owner_type_low = models.CharField(
        max_length=10, choices=owner_type_choices, default='0')
    owner_pp = models.ForeignKey(
        Citizen,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_companies'
    )
    owner_com = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_companies'
    )
    name_low = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    warehouse = models.BooleanField(default=True)
    registration_number = models.BigIntegerField(
        blank=True,
        unique=True,
        null=True,
        editable=False
    )
    established = models.DateField(auto_now_add=False)
    invoice_prefix = models.CharField(max_length=2, blank=False, unique=True)
    manufacturer_code = models.IntegerField(default=0, blank=True)
    street_adress_1 = models.IntegerField(default=0, blank=True, null=True)
    street_adress_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=7, blank=True)
    country = models.CharField(max_length=100, blank=True)
    employee_count = models.IntegerField(blank=True, default=0)
    total_salaries_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_bruto_salaries = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_vsaoi_dd = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_vsaoi_dn = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_iin = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_netto = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    average_salary_brutto = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)

    def __str__(self):
        return self.name_low

    def get_display_name(self):
        return self.name

    def get_house_number(self):
        return self.street_adress_1 or 0

    def clean(self):
        if bool(self.owner_pp) == bool(self.owner_com):
            raise ValidationError(
                "A company must have either a private person or another "
                "company as its owner, but not both or none."
            )

        if self.owner_pp and self.owner_type_low != '0':
            raise ValidationError(
                "If a private person is selected as the owner, the "
                "owner_type should be 'Private'."
            )
        if self.owner_com and self.owner_type_low != '1':
            raise ValidationError(
                "If another company is selected as the owner, the "
                "owner_type should be 'Company'."
            )

    # Signal sent to companies-signals
    def salaries_total(self):
        """
        Update total salaries each time a employee is added,
        or his salary has been changed.
        """
        print("Signal executed")
        self.total_bruto_salaries = self.employer.aggregate(
            Sum('salary_brutto'))['salary_brutto__sum'] or 0
        self.total_salary_vsaoi_dd = self.employer.aggregate(
            Sum('salary_vsaoi_dd'))['salary_vsaoi_dd__sum'] or 0
        self.total_salary_vsaoi_dn = self.employer.aggregate(
            Sum('salary_vsaoi_dn'))['salary_vsaoi_dn__sum'] or 0
        self.total_salary_iin = self.employer.aggregate(
            Sum('salary_iin'))['salary_iin__sum'] or 0
        self.total_salary_netto = self.employer.aggregate(
            Sum('salary_netto'))['salary_netto__sum'] or 0
        self.total_salaries_cost = self.total_bruto_salaries + self.total_salary_vsaoi_dd or 0  # noqa
        self.average_salary_brutto = self.total_bruto_salaries / self.employee_count if self.employee_count != 0 else 0  # noqa
        super().save()

    def save(self, *args, **kwargs):
        self.clean()
        if not self.registration_number:
            company_count = Company.objects.all().count() or 0
            self.registration_number = (
                "475010" + str(company_count + 1).zfill(4)
            )
        self.manufacturer_code = letter_to_number(self.name)
        self.name_low = remove_accents(self.name.replace(" ", "_")).lower()
        self.employee_count = CompanyEmployees.objects.filter(company=self.id).count() or 0  # noqa
        total_bruto_salaries = self.total_bruto_salaries or 0
        total_salary_vsaoi_dd = self.total_salary_vsaoi_dd or 0
        if not self.employee_count:
            self.total_salaries_cost = 0
            self.average_salary_brutto = 0
        else:
            self.total_salaries_cost = (
                total_bruto_salaries + total_salary_vsaoi_dd or 0
            )
            self.average_salary_brutto = (
                total_bruto_salaries / self.employee_count
            )
        super().save(*args, **kwargs)


class CompanyEmployees(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employer')
    name = models.ForeignKey(
        Citizen,
        on_delete=models.CASCADE,
        related_name='employee')
    role = models.CharField(max_length=254)
    salary_brutto = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    salary_vsaoi_dd = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    salary_vsaoi_dn = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    salary_iin = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    salary_netto = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the salary levels
        if it hasn't been set already.
        """
        # Fetch the latest settings
        latest_settings = get_object_or_404(AppSettings, valid=True)
        # Calculate the various components of the salary
        self.salary_vsaoi_dd = (self.salary_brutto / 100) * latest_settings.vsaoi_dd  # noqa
        self.salary_vsaoi_dn = (self.salary_brutto / 100) * latest_settings.vsaoi_dn  # noqa
        # Calculate IIN component, considering the no_iin_level
        taxable_amount = self.salary_brutto - self.salary_vsaoi_dn - latest_settings.no_iin_level  # noqa
        iin_calc = (taxable_amount / 100) * latest_settings.iin_rate
        # Set IIN based on calculated value, ensuring it's not less than 0
        self.salary_iin = max(iin_calc, 0)
        # Calculate net salary
        self.salary_netto = self.salary_brutto - self.salary_vsaoi_dn - self.salary_iin  # noqa
        # Call the parent save method to persist changes
        super().save(*args, **kwargs)


class GovInstitution(models.Model):

    class Meta:
        verbose_name_plural = 'Government Institutions'

    name_low = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True)
    registration_number = models.BigIntegerField(
        blank=True,
        unique=True,
        null=True,
        editable=False
    )
    established = models.DateField(auto_now_add=False)
    authority = models.CharField(max_length=100, blank=True)
    street_adress_1 = models.IntegerField(blank=True, null=True)
    street_adress_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=7, blank=True)
    country = models.CharField(max_length=100, blank=True)
    employee_count = models.IntegerField(blank=True)
    total_salaries_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_bruto_salaries = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_vsaoi_dd = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_vsaoi_dn = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_iin = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    total_salary_netto = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)
    average_salary_brutto = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True)

    def __str__(self):
        return self.name_low

    def get_display_name(self):
        return self.name

    def get_house_number(self):
        return self.street_adress_1 or 0

    def save(self, *args, **kwargs):
        if not self.registration_number:
            gov_inst__count = GovInstitution.objects.all().count() or 0
            self.registration_number = (
                "900010" + str(gov_inst__count + 1).zfill(4)
            )
        self.name_low = remove_accents(self.name.replace(" ", "_")).lower()
        self.employee_count = 0
        if not self.employee_count:
            self.total_salaries_cost = 0
            self.average_salary_brutto = 0
        else:
            self.total_salaries_cost = (
                self.total_bruto_salaries + self.total_salary_vsaoi_dd or 0
            )
            self.average_salary_brutto = (
                self.total_bruto_salaries / self.employee_count
            )
        super().save(*args, **kwargs)
