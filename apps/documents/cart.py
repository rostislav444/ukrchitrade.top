from django.core import serializers
from django.urls import reverse
from django.shortcuts import get_object_or_404
from project import settings
from apps.catalogue.models import Product

import time
import json
import datetime


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart
        keyDel = []
        for key, value in cart.items():
            try: ProductVariant.objects.get(pk=int(key))
            except: keyDel.append(key)
        for key in keyDel:
            del self.cart[key]
        self.save()

        for item in list(self.cart.values()):
            yield item

    def add(self, data):
        print(data)
        product = Product.objects.get(pk=int(data['id']))
        self.cart[product.pk] = {
            'id' : product.pk,
            'price' : product.price,
            'quantity' : data['quantity']
        }
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, color_id):
        if color_id in self.cart:
            del self.cart[color_id]
            self.save()


    def data(self):
        data = json.loads(json.dumps(self.cart, ensure_ascii=False).encode('utf8'))
        return data

    def total(self):
        total = {'quantity' : 0, 'total' : 0}
        for key in self.cart.keys():
            item = self.cart[key]
            total['quantity'] += int(item['quantity'])
            total['total'] += int(item['quantity']) * int(item['price'])
        return total

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


















# from project import settings
# from apps.shop.models import Product
# import time

# class Cart(object):
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart

#     def __iter__(self):
#         cart_list = []
#         # Convert to list
#         for i in self.cart.values():
#             cart_list.append(i)
#         # Sort by time
#         for num in range(len(cart_list)-1,-1,-1):
#                 for item in cart_list:
#                     if cart_list[num]['time'] > cart_list[num-1]['time']:
#                         temp = cart_list[num]
#                         cart_list[num] = cart_list[num-1]
#                         cart_list[num-1] = temp
#         # Generator
#         for i in cart_list:
#             yield i

#     def len(self):
#         return len(self.cart)

#     def total(self):
#         total = 0
#         for key in self.cart.keys():
#             total += self.cart[key]['price'] * self.cart[key]['quantity']
#         return total


#     def add(self, product, quantity, update_quantity=False):
#             product_id = str(product.pk)
#             if product_id in self.cart:
#                 if update_quantity==False:
#                     product_cur_qnt = int(self.cart[product_id]['quantity'])
#                     self.cart[product_id]['quantity'] = int(product_cur_qnt) + int(quantity)
#                 else:
#                     self.cart[product_id]['quantity'] = int(quantity)
#             else:
#                 self.cart[product_id] = {
#                     'id' : product_id,
#                     'name' : product.name,
#                     'code' : product.code,
#                     'image' : str(product.image1.url),
#                     'quantity' : int(quantity),
#                     'price' : product.price,
#                     'brand' : str(product.brand.name),
#                     'time' : int(time.time()),
#                     'url'  : str(product.get_absolute_url),
#                 }
#             self.save()


#     def remove(self, product_id):
#         product_id = str(product_id)
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()

#     def clear(self):
#         # remove car
#         del self.session[settings.CART_SESSION_ID]
#         self.save()


#     def save(self):
#         self.session.modified = True
