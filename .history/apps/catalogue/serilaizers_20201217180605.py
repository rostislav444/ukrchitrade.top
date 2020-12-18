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
    products =          serializers.IntegerField(read_only=True)
    products_filtered = serializers.IntegerField(read_only=True)
    count             = serializers.SerializerMethodField()
    selected =          serializers.BooleanField(read_only=True)
 
    class Meta:
        model = AttributeValue
        fields = [
            'pk','name','slug','count','selected','products','products_filtered'
        ]

    # self.context.get
    def get_count(self, obj):
        context = self.context
        params = self.context['params']
        category = self.context['category']
        pks = self.context['products'].values_list('id', flat=True)
        products = Product.objects.filter(product_attrs__value=obj, category__in=category.get_descendants(include_self=True)).distinct()
        filtered, extra = 0, 0
        if params:
            for key, value in params.items():
                if key != obj.parent.slug and key not in ['price_ua__gte', 'price_ua__lte']:
                    products = products.filter(
                        product_attrs__attribute__attribute__slug = key, 
                        product_attrs__value__slug__in = value,
                    )

        filtered = products.count()
        extra = products.exclude(id__in=pks).count()
        return {'filterd' : filtered, 'extra' : extra}


    
 
        

class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)
    
    class Meta:
        model = Attribute
        fields = ['pk','name','slug','values']



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


class ProductSearchSerializer(serializers.ModelSerializer):
    image =  serializers.CharField(label=_('Изобразение'),source='get_image')
    name =   serializers.CharField(label=_('Название'), source='trans.name')
    code =   serializers.CharField(label=_('Артикул'))
    price = serializers,CharField(source='get_price_ua')

    class Meta:
        model = Product
        fields = [
            'image', 'name', 'code'
        ]

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