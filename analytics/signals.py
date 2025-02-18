from .models import InvoiceAnalytics
from core.models import Invoice
from django.db.models.signals import post_save
from django.dispatch import receiver

# Signal to create or update InvoiceAnalytics when Invoice is saved
@receiver(post_save, sender=Invoice)
def create_or_update_invoice_analytics(sender, instance, **kwargs):
    analytics, created = InvoiceAnalytics.objects.get_or_create(invoice=instance)
    analytics.calculate_analytics()