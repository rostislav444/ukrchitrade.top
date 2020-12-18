from django.urls import include, path, re_path
from apps.cart import views


app_name = 'cart'


urlpatterns = [
    path('add',    views.CartView.as_view({'post' : 'add'}), name="add"),
    path('clear',  views.CartView.as_view({'get' : 'clear'}), name="clear"),
    path('remove', views.CartView.as_view({'post' : 'remove'}), name="remove"),
  
]
