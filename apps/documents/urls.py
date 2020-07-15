from django.urls import include, path, re_path
from apps.documents import views


app_name = 'documents'


cart = [
    path('add-update', views.CartAddUpdate, name='cart-add-update'),
    path('delete',     views.CartDelete,    name='cart-delete'),
    path('clear',      views.CartClear,     name='cart-clear'),
]

invoice = [
    path('update/',           views.InvoiceUpdate,  name='invoice-update'),
    path('update/<int:id>/',  views.InvoiceUpdate,  name='invoice-update'),
    path('get/',              views.InvoiceGet,    name='invoice-get'),
    path('get/<int:id>/',     views.InvoiceGet,    name='invoice-get'),
    path('print/',            views.InvoicePrint,  name='invoice-print'),
    path('print/<int:id>/',   views.InvoicePrint,  name='invoice-print'),
    # path('product-delete/<invoice>/<product>',   views.InvoiceProductDelete,  name='invoice-product-delete'),
    
]


urlpatterns = [
    path('invoice/',  include(invoice)),
    path('cart/',     include(cart))
]
