from rest_framework import serializers
from django.db import transaction
from .models import InvoiceAnalytics

class InvoiceAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceAnalytics
        fields = ['date','profit','profit_percentage','landed_cost','sale','miscellaneous','miscellaneous_percentage','carrier_charge_per_kilo','carrier_charge_percent']

class AnalyticsSerializer(serializers.Serializer):
    total_profit = serializers.SerializerMethodField()
    total_investment = serializers.SerializerMethodField()
    total_sale = serializers.SerializerMethodField()
    total_trips = serializers.SerializerMethodField()
    stats = InvoiceAnalyticsSerializer(many=True,read_only=True)
    
    def get_total_profit(self,obj):
        return sum(stat.profit for stat in obj['stats'])

    def get_total_investment(self,obj):
        return sum(stat.landed_cost for stat in obj['stats'])

    def get_total_sale(self,obj):
        return sum(stat.sale for stat in obj['stats'])

    def get_total_trips(self, obj):
        return InvoiceAnalytics.objects.count()