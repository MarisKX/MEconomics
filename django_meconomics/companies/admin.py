# Django imports
from django.contrib import admin

# Custom imports
from companies.models import Company


# Custom admin class for the Company model
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'warehouse',
        'registration_number',
        'established',
        'invoice_prefix',
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


# Register the Company model with the custom admin class
admin.site.register(Company, CompanyAdmin)
