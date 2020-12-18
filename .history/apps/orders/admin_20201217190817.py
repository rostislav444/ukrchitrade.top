from django.contrib import admin
from apps.orders.models import Order, OrderProduct


class OrderProduct(admin.StackedInline):
    model = Orderproduct

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProduct]
