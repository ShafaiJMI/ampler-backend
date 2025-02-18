from django.db import models
from core.models import Invoice

class InvoiceAnalytics(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name="analytics")
    date = models.DateField(auto_now_add=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    landed_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Investment
    sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Revenue
    miscellaneous = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    miscellaneous_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    carrier_charge_per_kilo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    carrier_charge_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def calculate_analytics(self):
        """Calculate profit, percentages, and other analytics fields"""
        if self.invoice:
            self.sale = self.invoice.bill_amount or 0
            self.landed_cost = self.invoice.landed_cost or 0
            self.profit = self.sale - self.landed_cost
            self.profit_percentage = (self.profit / self.landed_cost * 100) if self.landed_cost else 0
            self.miscellaneous = self.invoice.miscellaneous or 0
            self.miscellaneous_percentage = (self.miscellaneous / self.sale * 100) if self.sale else 0
            self.carrier_charge_per_kilo = self.invoice.carrier_charge or 0
            self.carrier_charge_percent = (self.carrier_charge_per_kilo / self.sale * 100) if self.sale else 0
            self.save()

