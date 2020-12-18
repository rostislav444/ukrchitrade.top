from django.shortcuts import render
from django.template.loader import render_to_string
from apps.shop.watchlist import WatchList
from django.http import JsonResponse
import json

def watchlist(request):
    watchlist = WatchList(request)
    
    template = 'shop/additions/watchlist/watchlist__products.html'
    html = render_to_string(template, {'products' : watchlist.data()})
    return JsonResponse({'html' : html, 'length' : len(watchlist.data())})