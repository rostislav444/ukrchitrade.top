from django.urls import reverse
from django.db.models import Value, PositiveIntegerField
from project import settings
from apps.catalogue.models import Product
from apps.cart.serializers import CartProductSerializer
import json


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {'products' : [], 'quantity' : 0, 'total' : 0}
        self.cart = cart
        

    def __iter__(self):
        for item in self.cart['products']:
            yield item

    def add(self, data):
        print(data)
        update =     data.get('update')
        product_id = data.get('product_id')
        quantity =   data.get('quantity')
        products =   self.cart.get('products')

        print(update)
        if product_id:
            product_exists = False
            for product in products:
                if product.get('product_id') == product_id:
                    product_exists = True
                    if update == True:
                        product['quantity'] = quantity
                    else:
                        product['quantity'] = int(quantity) + int(product['quantity'] )
            if product_exists == False:
                products.append(
                    {
                        'product_id' : product_id,
                        'quantity' : quantity
                    }
                )
        self.cart['products'] = products
        self.save()
        return self.data()
        


    def data(self):
        exclude = []
        cart_data = {
            'products' : [], 'quantity' : 0, 'total' : 0,
        }
        for item in self.cart['products']:
            product_id = item.get('product_id')
            product = Product.objects.filter(pk=product_id).annotate(
                quantity=Value(item['quantity'], output_field=PositiveIntegerField())
            ).first()
            if product:
                serializer = CartProductSerializer(product).data
                cart_data['quantity'] += serializer.get('quantity')
                cart_data['total'] += serializer.get('total')
                cart_data['products'].append(serializer)
        return cart_data

    def save(self):
        self.session.modified = True

    def remove(self, number):
        del self.cart['products'][int(number)]
        self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

