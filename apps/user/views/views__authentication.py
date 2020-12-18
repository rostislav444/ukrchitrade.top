from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import login, logout
from django.views import View

from apps.user.models import CustomUser
from apps.catalogue.models import Product
from apps.user.froms import LoginForm, RegistrationForm



class AuthenticationView(View):
    template_name = 'shop/user/authentication.html'
    context = {
        'forms' : {
            'login' : LoginForm(),
            'registration' : RegistrationForm(),
        }
    }


    def get(self, request, page=None, api=None):
        self.context['page'] = page
        return render(request, self.template_name, self.context)


    def post(self, request, page=None, api=None):
        self.context['page'] = page
        if page == 'login' or page == None:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = CustomUser.objects.get(email=form.cleaned_data['username'])
                login(request, user)
                return redirect(reverse('shop:home'))
        return render(request, self.template_name, self.context)


