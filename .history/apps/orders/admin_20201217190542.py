from django.contrib import admin
from apps.orders.models import Order, OrderProduct

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
