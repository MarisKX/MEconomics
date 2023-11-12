from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CompanyEmployees, GovInstEmployees


@receiver(post_save, sender=CompanyEmployees)
def update_company_on_save(sender, instance, **kwargs):
    """
    Update company total on lineitem update/create
    """
    instance.company.salaries_total()


@receiver(post_delete, sender=CompanyEmployees)
def update_company_on_delete(sender, instance, **kwargs):
    """
    Update company total on lineitem delete
    """
    instance.company.salaries_total()


@receiver(post_save, sender=GovInstEmployees)
def update_govinst_on_save(sender, instance, **kwargs):
    """
    Update government institution total on lineitem update/create
    """
    instance.gov_inst.salaries_total()


@receiver(post_delete, sender=GovInstEmployees)
def update_govinst_on_delete(sender, instance, **kwargs):
    """
    Update government institution total on lineitem delete
    """
    instance.gov_inst.salaries_total()
