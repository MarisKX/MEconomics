# Django imports
from django.db import models
# Other model imports
# Custom imports
from core.custom_functions.remove_accents import remove_accents


class Citizen(models.Model):

    class Meta:
        verbose_name_plural = 'Citizens'

    name = models.CharField(
        max_length=254,
        blank=True,
        null=True,
        editable=False
    )
    full_name = models.CharField(max_length=254)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    bsn_number = models.PositiveIntegerField(
        blank=True,
        unique=True,
        null=True,
        editable=False
    )
    street_adress_1 = models.IntegerField(blank=True, null=True)
    street_adress_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=6, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def get_house_number(self):
        return self.street_adress_1

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the citizen name and bsn
        if it hasn't been set already.
        """
        if not self.bsn_number:
            year = 1800  # Temporary setting !!!
            citizen_count = Citizen.objects.count() + 1
            self.bsn_number = int(f"{year}{citizen_count:04d}")

        # Format other fields if needed (e.g., names)
        first_name_low = remove_accents(
            self.first_name.replace(" ", "_")).lower()
        last_name_low = remove_accents(
            self.last_name.replace(" ", "_")).lower()
        self.name = f"{first_name_low}_{last_name_low}"
        self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)
