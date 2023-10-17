# Django imports
from django.contrib import admin
# Custom imports
from companies.models import (
    Company,
    GovInstitution,
)


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'warehouse',
        'registration_number',
        'established',
        'invoice_prefix',
        'employee_count',
        'total_salaries_cost',
    )
    readonly_fields = (
        'name_low',
        'registration_number',
        'manufacturer_code',
        'employee_count',
        'total_salaries_cost',
        'total_bruto_salaries',
        'total_salary_vsaoi_dd',
        'total_salary_vsaoi_dn',
        'total_salary_iin',
        'total_salary_netto',
        'average_salary_brutto',
    )


class GovInstitutionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'registration_number',
        'established',
        'authority',
        'employee_count',
        'total_salaries_cost',
    )
    readonly_fields = (
        'name_low',
        'registration_number',
        'employee_count',
        'total_salaries_cost',
        'total_bruto_salaries',
        'total_salary_vsaoi_dd',
        'total_salary_vsaoi_dn',
        'total_salary_iin',
        'total_salary_netto',
        'average_salary_brutto',
    )


# Register the Company model with the custom admin class
admin.site.register(Company, CompanyAdmin)
admin.site.register(GovInstitution, GovInstitutionAdmin)
