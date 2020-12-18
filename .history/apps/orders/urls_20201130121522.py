from django.urls import include, path, re_path
from django.views.generic import TemplateView
from apps.shop import views


app_name = 'shop'


catalogue = [
    re_path(
        # r'''^(?P<category>[^/]+)'''
        r'''(?:\/category:(?P<category>[^/]+))?'''
        r'''(?:\/selection:(?P<selection>[^/]+))?'''
        r'''(?:\/brand:(?P<brand>[^/]+))?'''
        r'''(?:\/color:(?P<color>[^/]+))?'''
        r'''(?:\/sizes:(?P<sizes>[^/]+))?'''
        r'''(?:\/filters:(?P<filters>[^/]+))?'''
        r'''(?:\/page:(?P<page>[\d+]+))?'''
        r'''(?:\/display:(?P<display>[\d+]+))?'''
        r'''(?:\/more:(?P<more>[\d+]+))?'''
        r'''(?:\/sort:(?P<sort>name:up|name:down|date:up|date:down|price:up|price:down|popularity:up|popularity:down))?/$''',
        views.CatalogueClass.as_view(), name="catalogue"
    ),
]

product = [
    path('comment/<product_slug>/id:<product_id>/variant_id:<variant_id>/', views.product_comment, name='product_comment'),
    path('category:<category>/brand:<brand>/<product_slug>/color:<color>/id:<product_id>/variant:<variant_id>/', views.product, name='product'),
]

cart = [
    path('add-update', views.CartAddUpdate, name='cart-add-update'),
    path('delete',     views.CartDelete,    name='cart-delete'),
    path('clear',      views.CartClear,     name='cart-clear'),
]


urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('catalogue',  include(catalogue)),
    path('xml_size/', views.catalogue_xml, name="catalogue_xml"),
    path('xml/', views.catalogue_xml_no_size, name="catalogue_xml_no_size"),
    path('xml_all/', views.catalogue_xml_all, name="catalogue_xml_all"),
    path('rozetka/', views.rozetka, name="rozetka"),

    path('product/',   include(product)),
    path('cart/',      include(cart)),
    # PAGES
    path('about',        TemplateView.as_view(template_name='shop/shop__about.html'),      name='about'),
    path('delivery',     TemplateView.as_view(template_name='shop/shop__delivery.html'),   name='delivery'),
    path('contacts',     TemplateView.as_view(template_name='shop/shop__contacts.html'),   name='contacts'),
    path('guarantee',    TemplateView.as_view(template_name='shop/shop__guarantee.html'),  name='guarantee'),
    path('public_offer', TemplateView.as_view(template_name='shop/shop__publicofer.html'), name="public_offer"),
    
   
    # path('fast-call',          views.fast_call,          name="fast_call"),
    # path('letter-to-director', views.letter_to_director, name="letter-to-director"),
    
    # path('news',               views.news,               name='news'),
    # path('news/<year>/<month>/<day>/<slug>', views.newsPostPage, name='news_post_page'),
]
