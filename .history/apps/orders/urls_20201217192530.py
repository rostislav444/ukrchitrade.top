from django.urls import include, path, re_path
from django.views.generic import TemplateView
from apps.orders import views


app_name = 'orders'


urlpatterns = [
    path('', views.home, name='order'),
   
]
