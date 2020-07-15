from django.urls import re_path, path, include
from apps.catalogue import views

app_name = 'catalogue'


urlpatterns = [
    path('', views.catalogue, name="catalogue"),
    re_path(r'^whoosale/(?P<size>small|middle|big|clean)/$', views.catalogue, name="whoosale"),
    path('export_excel/', views.export_excel, name="export_excel"),
    # re_path(r'^export_excel/(?P<price>\w+)?(/(?P<whoosale>small|middle|big)?)?', views.export_excel, name="export_excel"),
    path('product/<id>/', views.product, name="product"),
   
    path('products_zip/', views.products_zip, name="products_zip"),
    path('products_zip/<ids>', views.products_zip, name="products_zip"),
]

