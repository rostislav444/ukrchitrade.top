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


    def user_data(self, request):

        return render(request, 'shop/user/profile/profile__userdata.html')


    def user_orders(self, request):

        return render(request, 'shop/user/profile/profile__userdata.html')

