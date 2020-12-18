from django.shortcuts import render
from django.db.models import Q, Prefetch, Case, When, Count, Value, F,  ExpressionWrapper
from django.db.models.functions import Round
from django.db.models import IntegerField, BooleanField, CharField, TextField
from django.db.models import OuterRef, Subquery
from django.db.models.expressions import RawSQL
from django.views.generic import View
from apps.catalogue.models import Product, Category
from apps.catalogue_filters.models import Attribute, AttributeValue, CategoryAttribute, CategoryAttributeValue, ProductAttribute
from apps.catalogue.serilaizers import CategorySerializer, AttributeSerializer, AttributeValueSerializer, ProductSerializer
import json
import math


class Catalogue(View):
    context = {
        'sort_by' : ['price_asc','price_dsc','newest','popularity']
    }


    def get_categories(self, category):
        if category: 
            return category.get_descendants(include_self=True)
        return Category.objects.all()


    def get_attrs(self, category, params=None, products=None):
        
        query_params = {
            'category_values__parent__parent__in' : category.get_family(),
            'product_attrs__parent__category__in' : category.get_descendants(include_self=True),
        }
        attr_values = AttributeValue.objects.distinct().filter(**query_params)

        if params:
            attr_values = attr_values.annotate(
                selected=Case(When(params, then=Value(True)), default=Value(False), output_field=BooleanField(),),
            )
        attrs = Attribute.objects.distinct().filter(values__in=attr_values).prefetch_related(
            Prefetch('values', attr_values)
        )
        return attrs


    def get_selected_attrs(self, atributes=None):
        if atributes:
            params_attr, params_price, params  = Q(), {}, {}
            for attr in atributes.split('/'):
                try: key, value = attr.split('=')
                except: continue
                value = value.split(',')
                if key == 'price':
                    # params_attr |= Q(product_attrs__parent__price_ua__gte=int(value[0]))
                    # params_attr |= Q(product_attrs__parent__price_ua__lte=int(value[1]))
                    params_price['price_ua__gte'] = int(value[0])
                    params_price['price_ua__lte'] = int(value[1])
                else:
                    params_attr |= Q(parent__slug=key, slug__in=value)
                    params[key] = value
                    
            return params_attr, params_price, params
        else:
            return None, {}, {}


    def add_ua_price(self, products, params):
        products = products.filter(**params)
        return products


    def filter_products_attrs(self, products, params):
        if params:
            print(params)
            for key, value in params.items():
                if key in ['price_ua__gte', 'price_ua__lte']:
                    products = products.filter(**{key : value})
                else:
                    products = products.filter(
                        product_attrs__attribute__attribute__slug = key, 
                        product_attrs__value__slug__in = value,
                    )
            products = products.distinct()
        return products


    def set_price_range(self, params, context, products):
        lst_price_product = products.order_by('price').first()
        hst_price_product = products.order_by('-price').first()
        context['min_price'] =  int(lst_price_product.get_price_ua if lst_price_product else 0)
        context['max_price'] =  math.ceil(hst_price_product .get_price_ua if hst_price_product  else 1)
        gte = params['price_ua__gte'] if 'price_ua__gte' in params.keys() else context['min_price']
        lte = params['price_ua__lte'] if 'price_ua__lte' in params.keys() else context['max_price']
        context['price__gte'] = gte if gte >= context['min_price'] else context['min_price']
        context['price__lte'] = lte if lte <= context['max_price'] else context['max_price']
        return context

    def get_sorted(self, products, sort, on_page):
        order_by = {
            'newest'    : '-update',
            'popularity' : '-update',
            'price_asc' : 'price',
            'price_dsc' : '-price',
        }
        if sort:
            return products.order_by(order_by[sort])[:on_page]
        return products.order_by(order_by['newest'])[:on_page]
        

    def set_context(self, category=None, sort=None, atributes=None):
        context = self.context
        on_page = 24
        
        # Filter by categories
        category = Category.objects.filter(slug=category).first()
        categories = self.get_categories(category)
       
        category_products = Product.objects.filter(category__in=categories)

        # FIlter by attrs
        params_attr, params_price, params = self.get_selected_attrs(atributes)
        category_products = self.filter_products_attrs(category_products, params)
        attrs =    self.get_attrs(category, params_attr, category_products)
        attrs_serialized = AttributeSerializer(attrs, many=True, context={
            'products':category_products, 
            'category' : category,
            'params':params,
        }).data
        
        # Flter by price range
        products = category_products
        products = self.add_ua_price(category_products, params_price)
        context =  self.set_price_range(params_price, context, category_products)
        context['category'] =   category
        context['categories'] = categories
        context['products'] =   self.get_sorted(products,sort,on_page)
        context['attributes'] = json.loads(json.dumps(attrs_serialized))
        return context


    def get(self, request, category=None, sort=None, atributes=None):
        
        context = self.set_context(category, sort, atributes)
        return render(request, 'shop/catalogue/catalogue.html', context)


    def post(self, request, category=None, sort=None, atributes=None):
        category = Category.objects.filter(slug=category)
        context = self.set_context(category, atributes)
        return render(request, 'shop/catalogue/catalogue__product__list.html', context)