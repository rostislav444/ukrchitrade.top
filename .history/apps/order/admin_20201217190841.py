from django.contrib import admin
from apps.orders.models import Order, OrderProduct


class OrderProductAdmin(admin.StackedInline):
    model = OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductAdmin]
