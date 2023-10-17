"""
Database core models.
"""
# Django/DRF imports
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
# Custom imports
from core.custom_functions.today import today


class UserManager(BaseUserManager):
    """Manager for Users"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have a email address!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class AppSettings(models.Model):

    class Meta:
        verbose_name_plural = "Basic Settings"
        indexes = [
            models.Index(fields=["settings_number"]),
        ]

    settings_number = models.CharField(max_length=8)
    valid_from = models.DateField(auto_now_add=False)
    valid_till = models.DateField(auto_now_add=False)
    actions_per_day = models.PositiveIntegerField(default=1)
    vsaoi_dn = models.DecimalField(
        max_digits=4, decimal_places=2, blank=False, null=False)
    iin_rate = models.DecimalField(
        max_digits=4, decimal_places=2, blank=False, null=False)
    no_iin_level = models.DecimalField(
        max_digits=8, decimal_places=2, blank=False, null=False)
    uin_rate = models.DecimalField(
        max_digits=4, decimal_places=2, blank=False, null=False)
    enviroment_tax_base = models.DecimalField(
        max_digits=8, decimal_places=2, blank=False, null=False)
    btw = models.DecimalField(
        max_digits=8, decimal_places=2, blank=False, null=False)
    vsaoi_dd = models.DecimalField(
        max_digits=4, decimal_places=2, blank=False, null=False)
    base_cadastre_value = models.DecimalField(
        max_digits=4, decimal_places=2, blank=False, null=False)
    valid = models.BooleanField()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the settings number
        if it hasn't been set already.
        """
        if not self.settings_number:
            self.valid = True
            settings_count = AppSettings.objects.all().count()
            if settings_count > 0:
                previous_settings = AppSettings.objects.latest('valid_till')
                previous_settings.valid = False
                previous_settings.save(update_fields=['valid'])
                print(previous_settings.valid)
            self.settings_number = str(
                today().year) + str(
                    settings_count + 1).zfill(4)
        super().save(*args, **kwargs)
