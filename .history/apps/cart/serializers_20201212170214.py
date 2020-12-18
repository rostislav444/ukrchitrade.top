from django.utils.translation import gettext as _
from rest_framework import serializers
from apps.catalogue.models import Product, Category



class CartProductSerializer(serializers.ModelSerializer):
    image =    serializers.CharField(source='get_image')
    quantity = serializers.IntegerField(label=_('Колличество'))
    price =    serializers.SerializerMethodField(label=_('Цена'))
    total =    serializers.SerializerMethodField(label=_('Всего'))

    class Meta:
        model = Product
        fields = [
            'id','name','image','quantity','price','total'
        ]

    def get_price(self, obj):
        price = obj.get_quantity_price(obj.quantity)
        if int(price) == price:
            return int(price)
        return price

    
    def get_total(self, obj):
        if obj:
            total = obj.get_quantity_price(obj.quantity) * obj.quantity
            if int(total) == total:
                return int(total)
            return total
        return 0