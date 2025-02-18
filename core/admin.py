from django.contrib import admin
from .models import *

# Register your models here.
class SellerAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number']
    list_editable = ['phone_number']
    list_display_links = ('name',)

class BuyerAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number']
    list_editable = ['phone_number']
    list_display_links = ('name',)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['date']

class SellAdmin(admin.ModelAdmin):
    list_display = ['date']

class PurchaseInline(admin.TabularInline):
    model = Purchase

class SellInline(admin.TabularInline):
    model = Sell


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number','seller','buyer','carrier_charge','advance_recived','total_amount','bill_amount','landed_cost']
    list_editable = ['carrier_charge','advance_recived']
    inlines = [
        SellInline,
        PurchaseInline,
    ]

admin.site.register(Invoice,InvoiceAdmin)
admin.site.register(Seller,SellerAdmin)
admin.site.register(Buyer,BuyerAdmin)
admin.site.register(Sell,SellAdmin)
admin.site.register(Purchase,PurchaseAdmin)

admin.site.site_header = "Ampler Mettle Invoices"  # Top left title
admin.site.site_title = "Ampler Mettle Invoices"  # Browser tab title
admin.site.index_title = "Ampler Mettle Invoice Application" 