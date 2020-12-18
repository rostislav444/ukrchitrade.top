from django.shortcuts import render
from apps.catalogue.models import Product
from apps.catalogue.serilaizers import ProductSerializer
from Levenshtein import StringMatcher as sm
from django.http import JsonResponse
from fuzzywuzzy import fuzz
from operator import itemgetter
import json, math
from django.views import View


class SearchView(View):
    context = {}

    def match(self, inp, val):
        wmtch = 0
        inps, vals = inp.split(' '), val.split(' ')
        for iw in inps:
            for vw in vals:
                ratio = max(
                    [fuzz.ratio(iw,vw), 
                    fuzz.ratio(iw,vw[:len(iw)+1])
                ])
                if ratio > 45:
                    wmtch += ratio
                    break
        return wmtch

    def match_products(self, param):
        products = []
        if param:
            for product in list(Product.objects.all()):
                ratio = self.match(param.lower(), product.name.lower())
                if ratio >= 65:
                    prod = ProductSerializer(product).data
                    prod['ratio'] = ratio
                    products.append(prod) 
            products = sorted(products, key=itemgetter('ratio'), reverse=True)
        return products

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        param = data.get('param')
        products = self.match_products(param)
        return JsonResponse({'param' : str(products)})

    def get(self, request):
        param = request.GET.get('param')
        return render(request, 'shop/search/search__popup_results.html', context)



def search(request):
    context = {}
    on_page = 12
  
    def MatchProdutcs(search_input):
        products = []
        
        def match(inp,val):
            wmtch = 0
            inps = inp.split(' ')
            vals = val.split(' ')
            for iw in inps:
                for vw in vals:
                    ratio = max([fuzz.ratio(iw,vw), fuzz.ratio(iw,vw[:len(iw)+1])])
                    if ratio > 45:
                        wmtch += ratio
                        break
            return wmtch

        if search_input:
            for product in list(Product.objects.all()):
                ratio = match(search_input.lower(), product.name.lower())
                if ratio >= 65:
                    prod = ProductSerializer(product).data
                    prod['ratio'] = ratio
                    products.append(prod) 
            products = sorted(products, key=itemgetter('ratio'), reverse=True)
        
        context['products'] = json.loads(json.dumps(products))
        context['search_input'] = search_input if search_input else ''
        context['products_len'] = len(products)
        context['pages'] = math.ceil(context['products_len'] / 12)
    
        request.session['search_context'] = context.copy()
        return context

    search_input = request.GET.get('param')
    context['param'] = search_input
    context = MatchProdutcs(search_input)
    context['products'] = context['products'][:on_page]
    return render(request, 'shop/search/search__popup_results.html', context)

