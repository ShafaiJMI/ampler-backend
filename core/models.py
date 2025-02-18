from django.db import models
from django.core.validators import RegexValidator
from datetime import date

# Create your models here.
  
class Seller(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(
        max_length=15,null=True,blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    address = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

class Buyer(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.CharField(
        max_length=15,null=True,blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    address = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

class MetalDetails(models.Model):
    METAL_CHOICES = [
        ('heavy', 'Heavy'),
        ('dehati', 'Dehati'),
        ('light', 'Light'),
        ('teena', 'Teena'),
        ('dust', 'Dust'),
    ]
    metal_type = models.CharField(max_length=20)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # e.g., in grams or kilograms
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)    # e.g., per gram or kilogram
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # Calculated field

    class Meta:
        abstract = True  # This makes MetalDetails an abstract base class

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    report_date = models.DateField(auto_now_add=True)
    purchase_date = models.DateField(auto_now_add=False,null=True, blank=True)
    sale_date = models.DateField(auto_now_add=False,null=True, blank=True)
    seller = models.ForeignKey(Seller, related_name='invoice',on_delete=models.CASCADE, null=True, blank=True) # Relationships with seller
    buyer = models.ForeignKey(Buyer, related_name='invoice',on_delete=models.CASCADE, null=True, blank=True) # Relationships with buyer
    oversize = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # oversize deduction from total sale at selling result will be bill amount
    # Expenses
    carrier_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loading = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    roadclearance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Total of all expense
    food = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    site_visit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    petrol = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    toll_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Final Amounts
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Total Amount of all Items i.e Items Weight x Rate
    miscellaneous = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Total Sale Amount (after oversize deduction)
    landed_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #
    benifit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Benifit = bill - total
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dues = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    advance_recived = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.report_date}"

    def generate_invoice_number(self):
        """Generate a unique invoice number."""
        today = date.today().strftime("%Y%m%d")  # Format: YYYYMMDD
        return f"INV-{today}-{self.pk}"

    def calculate_miscellaneous(self):
        fields = [
            self.carrier_charge, self.loading, self.roadclearance,
            self.food, self.site_visit, self.extra_expense,
            self.petrol, self.toll_tax
            ]
        total = sum(field or 0 for field in fields)
        return total

    def calculate_total(self):
        """Calculate total amount from all purchase items."""
        self.total_amount = sum(purchase.amount for purchase in self.purchases.all())

    def calculate_bill_amount(self):
        """Calculate total sale amount and deduct oversize if applicable."""
        total_sale = sum(sale.amount for sale in self.sales.all())
        return total_sale - (self.oversize or 0)

    def calculate_landedcost(self):
        """Calculate total landed cost (total amount + miscellaneous)."""
        return (self.total_amount or 0) + (self.miscellaneous or 0)

    def calculate_benifit(self):
        """Calculate benefit as the difference between bill amount and landed cost."""
        return (self.bill_amount or 0) - (self.landed_cost or 0)

    #add features to drop related tables when invoice creation fails
    def create_default_items(self):
        """Creates default items with zero weight for both purchase and sale."""
        metals = ['heavy', 'dehati', 'light', 'teena', 'CI', 'dust']

        for metal in metals:
            purchase_item = Purchase.objects.create(metal_type=metal)
            sale_item = Sell.objects.create(metal_type=metal)
            self.purchases.add(purchase_item)
            self.sales.add(sale_item)
    

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        super().save(*args, **kwargs)
        if is_new and not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
            
            super().save(update_fields=["invoice_number"])   # Save only the updated field
        

class Purchase(MetalDetails):
    invoice = models.ForeignKey(Invoice, related_name="purchases", on_delete=models.CASCADE, null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)


class Sell(MetalDetails):
    invoice = models.ForeignKey(Invoice, related_name="sales", on_delete=models.CASCADE, null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)