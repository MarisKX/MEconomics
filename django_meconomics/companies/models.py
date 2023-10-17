# Django imports
from django.db import models
from django.core.exceptions import ValidationError
# Other model imports
from citizens.models import Citizen
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

        if self.owner_pp and self.owner_type != '0':
            raise ValidationError(
                "If a private person is selected as the owner, the "
                "owner_type should be 'Private'."
            )
        if self.owner_com and self.owner_type != '1':
            raise ValidationError(
                "If another company is selected as the owner, the "
                "owner_type should be 'Company'."
            )

    def save(self, *args, **kwargs):
        self.clean()
        if not self.registration_number:
            company_count = Company.objects.all().count() or 0
            self.registration_number = (
                "475010" + str(company_count + 1).zfill(4)
            )
        self.manufacturer_code = letter_to_number(self.name)
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
