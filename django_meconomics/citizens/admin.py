"""
Django admin customization
"""
# Django imports
from django.contrib import admin
# Custom imports
from citizens.models import Citizen


class CitizenAdmin(admin.ModelAdmin):
    readonly_fields = (
        'name',
        'first_name_low',
        'last_name_low',
        'bsn_number',
        'id',
    )
    list_display = (
        'first_name',
        'last_name',
        'bsn_number',
    )

    ordering = ('bsn_number',)


admin.site.register(Citizen, CitizenAdmin)
