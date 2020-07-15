from django.urls import include, path, re_path
from apps.core import views


app_name = 'core'


pages = [
    path('about',        views.PageAboutView,       name='page_about'),
    path('delivery',     views.PageDeliveryView,    name='page_delivery'),
    path('returns',      views.PageReturnsView,     name='page_returns'),
    path('guarantee',    views.PageGuaranteeView,   name='page_guarantee'),
    path('public_offer', views.PagePublicOfferView, name='page_public_offer'),
    path('contacts',     views.Contacts,            name='contacts'),
    path('policy',       views.Policy,              name='policy'),
]


urlpatterns = [
    path('pages/',  include(pages)),
]
