# serializers.py
from rest_framework import serializers
from django.db import transaction
from .models import Seller, Buyer, MetalDetails, Invoice, Purchase, Sell

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class MetalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetalDetails
        fields = '__all__'

class PurchaseSerializer(MetalDetailsSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class SellSerializer(MetalDetailsSerializer):
    class Meta:
        model = Sell
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(many=False)
    buyer = BuyerSerializer(many=False)
    purchases = PurchaseSerializer(many=True)
    sales = SellSerializer(many=True)

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        seller_data = validated_data.pop('seller')
        buyer_data = validated_data.pop('buyer')
        purchases_data = validated_data.pop('purchases')
        sales_data = validated_data.pop('sales')

        with transaction.atomic():
            seller, _ = Seller.objects.get_or_create(**seller_data) # Check if seller already exist
            buyer, _ = Buyer.objects.get_or_create(**buyer_data) # Check if Buyer already exist
            invoice = Invoice.objects.create(seller=seller, buyer=buyer, **validated_data)
            
            # Create purchases and sales items
            for purchase_data in purchases_data:
                Purchase.objects.create(invoice=invoice, **purchase_data)
            for sale_data in sales_data:
                Sell.objects.create(invoice=invoice, **sale_data)

        return invoice
    
class InvoiceListSerializer(serializers.ModelSerializer):
    seller_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['invoice_number','report_date','seller_name','buyer_name','landed_cost']

    def get_seller_name(self, obj):
        return obj.seller.name

    def get_buyer_name(self, obj):
        return obj.buyer.name