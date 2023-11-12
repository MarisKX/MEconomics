# Django imports
from django.contrib import admin
# Custom imports
from companies.models import (
    Company,
    GovInstitution,
    CompanyEmployees,
    GovInstEmployees,
    Warehouse,
)


class CompanyEmployeesAdmin(admin.TabularInline):
    model = CompanyEmployees
    readonly_fields = (
        'salary_vsaoi_dd',
        'salary_vsaoi_dn',
        'salary_iin',
        'salary_netto',
        )
    list_display = (
        'company',
        'name',
        'salary_brutto'
    )

    ordering = ('name',)


class CompanyAdmin(admin.ModelAdmin):
    inlines = (CompanyEmployeesAdmin, )
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


class GovInstEmployeesAdmin(admin.TabularInline):
    model = GovInstEmployees
    readonly_fields = (
        'salary_vsaoi_dd',
        'salary_vsaoi_dn',
        'salary_iin',
        'salary_netto',
        )
    list_display = (
        'gov_inst',
        'name',
        'salary_brutto'
    )

    ordering = ('name',)


class GovInstitutionAdmin(admin.ModelAdmin):
    inlines = (GovInstEmployeesAdmin, )
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


class WahrehouseAdmin(admin.ModelAdmin):
    list_display = (
        'name_low',
        'name',
        'warehouse_code',
        "street_adress_1",
        "street_adress_2",
        "city",
        "post_code",
        'country',
    )
    readonly_fields = (
        'name_low',
    )


# Register the Company model with the custom admin class
admin.site.register(Company, CompanyAdmin)
admin.site.register(GovInstitution, GovInstitutionAdmin)
admin.site.register(Warehouse, WahrehouseAdmin)
