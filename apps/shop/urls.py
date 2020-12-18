from django.urls import re_path, path, include
from apps.shop import views

app_name = 'shop'


urlpatterns = [
    path('', views.home, name="home"),
    path('watchlist', views.watchlist, name="watchlist"),
    re_path(
        r'''^catalogue/(?P<category>[\w-]+)/?(?:\/(?P<sort>price_asc|price_dsc|newest|popularity)/)?'''
        # r'''?(sort-by-(?P<sort>price_asc|price_dsc|newest|popularity))?/'''
        r'''?(?:\/filter/(?P<atributes>[-=,\w/]*))?$''',
        views.Catalogue.as_view(), 
        name="catalogue"
    ),
    re_path(
        r'''^catalogue/(?P<category>[\w-]+)/product-(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/'''
        r'''?(?:\/(?P<page>characteristics|comments|questions|certificates|))?/?$''',
        views.ProductPage.as_view({'get':'page'}), 
        name="product"
    ),
    re_path(
        r'''^catalogue/(?P<category>[\w-]+)/product-(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/'''
        r'''?(?:\/(?P<page>comment_form))?/?$''',
        views.ProductPage.as_view({'post':'comment_form'}), 
        name="comment_form"
    ),
     re_path(
        r'''^catalogue/(?P<category>[\w-]+)/product-(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/'''
        r'''?(?:\/(?P<page>question_form))?/?$''',
        views.ProductPage.as_view({'post':'question_form'}), 
        name="question_form"
    ),



    
]

