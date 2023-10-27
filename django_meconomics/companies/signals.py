from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CompanyEmployees


@receiver(post_save, sender=CompanyEmployees)
def update_on_save(sender, instance, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.company.salaries_total()


@receiver(post_delete, sender=CompanyEmployees)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.company.salaries_total()
