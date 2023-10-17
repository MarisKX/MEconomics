"""
Django admin customization
"""
# Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# Custom imports
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class AppSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ('settings_number',)
    list_display = (
        'settings_number',
        'actions_per_day',
        'valid',
        'valid_from',
        'valid_till',
        'no_iin_level',
        'enviroment_tax_base',
        'btw',
    )

    ordering = ('settings_number',)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.AppSettings, AppSettingsAdmin)
