from django.contrib import admin
from apps.order.models import Order, OrderProduct


class OrderProductAdmin(admin.StackedInline):
    model = OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductAdmin]
