from django.contrib import admin
from .models import InvoiceAnalytics

# Register your models here.
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ['id','date','profit','sale','landed_cost']
    list_display_links = ('id',)

admin.site.register(InvoiceAnalytics,AnalyticsAdmin)