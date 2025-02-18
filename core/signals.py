from .models import Purchase,Sell
from django.db.models.signals import post_save
from django.dispatch import receiver

# Signal to create or update InvoiceAnalytics when Invoice is saved
@receiver(post_save, sender=Purchase)
def update_invoice_on_purchase_save(sender, instance, **kwargs):
    invoice = instance.invoice
    #total_amount = invoice.objects.aggregate(total=Sum(F('weight') * F('rate')))['total'] or 0.00
    if invoice:
        invoice.total_amount = sum(purchase.weight * purchase.rate for purchase in invoice.purchases.all()) or 0.00
        invoice.save()

@receiver(post_save, sender=Sell)
def update_invoice_on_sell_save(sender, instance, **kwargs):
    invoice = instance.invoice
    #total_amount = invoice.objects.aggregate(total=Sum(F('weight') * F('rate')))['total'] or 0.00
    if invoice:
        invoice.bill_amount = sum(sale.weight * sale.rate for sale in invoice.sales.all()) or 0.00
        invoice.save()