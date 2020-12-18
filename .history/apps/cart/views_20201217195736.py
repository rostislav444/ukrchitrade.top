from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from .cart import Cart
from django.views.decorators.http import require_http_methods
import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



class CartView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    products_tpl = "shop/cart/cart_products.html"

    def initial(self, request, *args, **kwargs):
        self.cart = Cart(request)
        super(CartView, self).initial(request, *args, **kwargs)

    def data(self, request):
        data = self.cart.data()
        html = render_to_string(self.products_tpl, {'cart' : data})
        data = {
            'total' : 500,
            'quantity' : data['quantity'],
            'html' :  html
        }
        return Response(data)

    def add(self, request):
        self.cart.add(request.data)
        return self.data(request)

    def clear(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect('/')

    def remove(self, request):
        cart = Cart(request)
        data = request.data
        cart.remove(int(data.get('product_id')))
        return self.data(request)
        
        


