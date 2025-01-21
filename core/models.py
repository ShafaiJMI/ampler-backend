from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
  
class Seller(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    address = models.TextField()

class Buyer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    address = models.TextField()

class MetalDetails(models.Model):
    METAL_CHOICES = [
        ('heavy', 'Heavy'),
        ('dehati', 'Dehati'),
        ('light', 'Light'),
        ('teena', 'Teena'),
        ('dust', 'Dust'),
    ]
    metal_type = models.CharField(max_length=20, choices=METAL_CHOICES)
    weight = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., in grams or kilograms
    rate = models.DecimalField(max_digits=10, decimal_places=2)    # e.g., per gram or kilogram
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)  # Calculated field

    class Meta:
        abstract = True  # This makes MetalDetails an abstract base class

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
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
    miscellaneous = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Total sale amount (after oversize deduction)
    total_landed_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #
    benifit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Benifit = bill - total
    advance_recived = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.date}"

    def calculate_miscellaneous(self):
        pass
    def calculate_landedcost(self):
        pass
    def calculate_bill_amount(self):
        pass
    def calculate_benifit(self):
        pass

    def create_default_items(self):
        """Creates default items with zero weight for both purchase and sale."""
        metals = ['heavy', 'dehati', 'light', 'teena', 'CI', 'dust']
        for metal in metals:
            purchase_item = Purchase.objects.create(metal_type=metal, date=self.date)
            sale_item = Sale.objects.create(metal_type=metal, date=self.date)
            self.purchases.add(purchase_item)
            self.sales.add(sale_item)

    def save(self, *args, **kwargs):
        self.miscellaneous = calculate_miscellaneous


class Purchase(MetalDetails):
    invoice = models.ForeignKey(Invoice, related_name="purchases", on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "purchases"


class Sell(MetalDetails):
    invoice = models.ForeignKey(Invoice, related_name="sales", on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "sales"