from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.user.models import Wishlist, CustomUser
from apps.catalogue.models import Product


class ProfileViewsSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def data(self, request):
        if request.user.is_authenticated:
            html = render_to_string('shop/additions/whishlist/wishlist__body.html', {'request' : request})
            html = html.replace('  ','').replace('\n','')
            return Response({'html' : html, 'length' : Wishlist.objects.filter(user=request.user).count()})
        return Response({'html' : "", 'length' : 0})
        

    def add(self, request):
        ajax = request.data.get('ajax')
        user = request.user
        if user.is_authenticated:
            product_id = request.data.get('product_id')
            product = Product.objects.filter(pk=product_id).first()
            if product:
                try:
                    Wishlist.objects.get(user=user, product=product)
                except:
                    wish = Wishlist(user=user, product=product)
                    wish.save()
            html = render_to_string('shop/additions/whishlist/wishlist__body.html', {'request' : request})
            if ajax:
                return Response({'html':html, 'length' : Wishlist.objects.filter(user=user).count()})
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            if ajax:
                Response({'error':'Вы не авторизованы в системе'})
            return redirect('/')


    def remove(self, request):
        ajax = request.data.get('ajax')
        user = request.user
        if user.is_authenticated:
            product_id = request.data.get('product_id')
            product = Wishlist.objects.filter(user=user, product__pk=int(product_id)).delete()
            html = render_to_string('shop/additions/whishlist/wishlist__body.html', {'request' : request})
            if ajax:
                return Response({'html':html, 'length' : Wishlist.objects.filter(user=user).count()})
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            if ajax:
                Response({'error':'Вы не авторизованы в системе'})
            else:
                return redirect('/')
            

