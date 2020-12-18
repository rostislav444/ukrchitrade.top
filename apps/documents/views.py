from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.timezone import get_current_timezone
from django.db import IntegrityError
from datetime import datetime
import json
from datetime import datetime
import pytz
# app
from apps.documents.models import *
from apps.catalogue.models import Product
from apps.catalogue.serilaizers import ProductSerializer
# drf
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import *
from .cart import Cart
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods('POST')
def InvoiceUpdate(request, id=0):
    data = json.loads(json.loads(request.body.decode("utf-8")))

    if len(data['code']) == 0:
        return JsonResponse(json.dumps({'error' : 'Введите номер инвойса'}), safe=False)

    # DATE
    try: date = datetime.strptime(data['date'], '%d.%m.%Y')
    except:
        return JsonResponse(json.dumps({'error' : 'Дата остуствует или не корректна'}), safe=False)
    context = {
        'template' : InvoiceTemplate.objects.get(pk=int(data['template'])),
        'exporter' : Company.objects.get(pk=int(data['exporter'])) if int(data['exporter']) != 0 else None,
        'importer' : Company.objects.get(pk=int(data['exporter'])) if int(data['importer']) != 0 else None,
        'incoterms' : Incoterms.objects.get(pk=int(data['incoterms'])) if int(data['incoterms']) != 0 else None,
        'price' :    PriceFormula.objects.get(pk=int(data['price'])),
        'date' :     date.date(),
        'code' :     data['code'],
    }

    
    if id == 0:
        invoice = Invoice(**context)
    else:
        invoice = Invoice.objects.get(pk=id)
        for key, value in context.items():
            setattr(invoice, key, value)

    try: invoice.save()
    except:
        return JsonResponse(json.dumps({'error' : 'Инвойс с таким номером уже сужествует'}), safe=False)
    

    productsIds = [int(product['id']) for product in data['products']]
    InvoiceProducts.objects.filter(invoice=invoice).exclude(pk__in=productsIds).delete()
    

    for item in data['products']:
        product = Product.objects.get(pk=int(item['id']))
        print(item['quantity'])
        try:
            invoiceProduct = InvoiceProducts.objects.get(product=product, invoice=invoice)
            setattr(invoiceProduct, 'quantity', int(item['quantity']))
        except:
            invoiceProduct = InvoiceProducts(product=product, invoice=invoice, quantity=int(item['quantity']))
        invoiceProduct.save()

    invoice =  InvoiceSerializer(invoice)
   
    response = {'invoice' : invoice.data }
    
    return JsonResponse(json.dumps(response), content_type='application/json', safe=False)


@csrf_exempt
@require_http_methods('GET')
def InvoiceGet(request, id=0):
    if id == 0:
        invoice = Invoice()
        invoice = InvoiceSerializer(invoice)
    else:
        invoice =  InvoiceSerializer(Invoice.objects.get(pk=id))
    
    response = {'invoice' : invoice.data }
    return JsonResponse(json.dumps(response), content_type='application/json', safe=False)


@csrf_exempt
@require_http_methods('GET')
def InvoicePrint(request, id=0):
    invoice = Invoice.objects.get(pk=id)
    filename = invoice.generate()
    return JsonResponse({'url' : filename, 'filename':filename.split('/')[-1] })


@csrf_exempt
@require_http_methods('GET')
def InvoiceProductDelete(invoice, product):
    product = InvoiceProducts.objects.get(invoice__pk=int(invoice), product__pk=int(product))
    product.delete()
    invoice =  InvoiceSerializer(Invoice.objects.get(pk=id))
    return


# CART
def ReturnCartData(request, url=None):
    # variant = ProductVariant.objects.get(pk=int(data['variant_id']))
    cart = Cart(request)
    cart.total = cart.total()
    response = {
        'url'   : 'cart',
      
    }
    response = json.dumps(response, ensure_ascii=False).encode('utf8')
    response = json.loads(response.decode('utf8'))
    return JsonResponse(response, safe=False)


@csrf_exempt
def CartAddUpdate(request, update=False):
    if request.method == 'POST':
        cart = Cart(request)
        data = json.loads(request.body.decode())
        cart.add(data)
        print('RESPONSE')
        return ReturnCartData(request)
    else:
        return HttpResponse(status=500)


@csrf_exempt
def CartDelete(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        cart = Cart(request)
        cart.remove(data['variant_id'])
        return ReturnCartData(request)
    else:
        return HttpResponse(status=500)
        

@csrf_exempt
def CartClear(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponse(status=200)
    if request.method == 'POST':
        return HttpResponse(status=200)
    else:
        referer = request.META.get('HTTP_REFERER')
        if referer is not None:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('/')