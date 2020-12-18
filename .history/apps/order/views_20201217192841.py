from django.shortcuts import render

# Create your views here.
def order(request):
    return render(request, 'shop/order/order.html')