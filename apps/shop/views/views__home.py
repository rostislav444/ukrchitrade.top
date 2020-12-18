from django.shortcuts import render


def home(request):
    return render(request, 'shop/home/home.html')