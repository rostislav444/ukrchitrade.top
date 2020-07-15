from rest_framework import routers, serializers, viewsets
from apps.catalogue_filters.models import Attribute, AttributeValue, CategoryAttribute,CategoryAttributeValue
from apps.catalogue.models import Product, Category
from django.utils.translation import gettext as _
from django.utils.translation import get_language as lang
from datetime import datetime


# CATEGORY
class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='translate.name') 
    description = serializers.CharField(source='translate.description') 

    class Meta:
        model = AttributeValue
        fields = ['name','description']


# ATRIBUTES
class AttributeValueSerializer(serializers.ModelSerializer):
    value = serializers.CharField(read_only=True, source="name")
    selected = serializers.SerializerMethodField()

    class Meta:
        model = AttributeValue
        fields = ['pk','value','selected']

    def get_selected(self, object):
        # for inst in self.instance:
        #     print(inst.count)
        if object.pk in self.context.get('selected'):
            return True
        return False

class AttributeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    values = serializers.SerializerMethodField() 
    # values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ['name','values']


    def get_values(self, object):
        q = self.__dir__()
        

        qs = AttributeValue.objects.filter(parent=object, pk__in=self.context.get('attr_values'))
        serializer = AttributeValueSerializer(qs, many=True, read_only=True, context={'selected' : self.context['selected']}).data
        return serializer

# PRODUCTS
class ProductSerializer(serializers.ModelSerializer):
    image =        serializers.CharField(label=_('Картинка'))
    category =     serializers.CharField(label=_('Категория'), source='category.trans.name')
    product_type = serializers.CharField(label=_('Тип товара'))
    code =         serializers.CharField(label=_('Артикул'))
    customs_code = serializers.CharField(label=_('УКТЗЕД'))
    name =         serializers.CharField(label=_('Название'), source='trans.name')
    price =        serializers.SerializerMethodField(label=_('Цена'), source='get_price')
    manufacturer = serializers.CharField(label=_('Производитель'), source='trans.manufacturer')
    has_fda = serializers.CharField()
    has_ce = serializers.CharField()
    price_update = serializers.SerializerMethodField(label=_('Обновление цены'))

    class Meta:
        model = Product
        fields = [
            'pk','image','category', 'product_type', 'code', 'customs_code','name', 'price', 'manufacturer', 
            'pieces_in_box','pieces_in_pack','update','has_fda','has_ce','has_description','get_absolute_url',
            'update', 'price_update', 'get_sm_start', 'get_md_start', 'get_bg_start', 'get_sm_price', 'get_md_price', 'get_bg_price', 
        ]

    def get_price(self, obj):
        price = obj.price
        if 'whoosale' in self.context and self.context['whoosale'] is not None:
            whoosale = {'small':'sm', 'middle':'md', 'big':'bg'}
            price = getattr(obj, f"get_{whoosale[self.context['whoosale']]}_price")
        if obj.price_box:
            price = price / obj.pieces_in_box
            return round(float(price), 4)
        return round(float(price), 2)

    def get_price_update(self, object):
        date = object.price_update.strftime('%d-%m-%Y')
        return date


class ProductCartSerializer(ProductSerializer):
    quantity = serializers.SerializerMethodField(label=_('Колличество'))
    total =    serializers.SerializerMethodField(label=_('Всего'))

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['quantity', 'total']

    def get_quantity(self, obj):
        # self.context['whoosale']
        return 5
    
    def get_total(self, obj):
        return 