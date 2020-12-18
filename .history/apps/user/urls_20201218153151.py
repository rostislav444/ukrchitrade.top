from django.urls import include, path, re_path
from apps.user import views

app_name = 'user'

wishlist = [
    path('',        views.WishlistViewsSet.as_view({'get': 'data'}),    name='wishlist'),
    path('add/',    views.WishlistViewsSet.as_view({'post': 'add'}),    name='wishlist_add'),
    path('remove/', views.WishlistViewsSet.as_view({'post': 'remove'}), name='wishlist_remove'),
]

authentication = [
    # re_path(r"^((?P<api>api)/)?$",           views.AuthenticationViewsSet.as_view({'get':'login',   'post':'login'}),    name='login'),
    re_path(
        r"^?((?P<page>login|registration)/)?/?((?P<api>api)/)?$", 
        views.AuthenticationView.as_view(), 
        name='authentication'),
]

profile = [
    path('', views.ProfileViewsSet.as_view({'get': 'user_data'}), name='user_data'),
]

urlpatterns = [
    path('whishlist/',  include(wishlist)),
    path('authntication/', include(authentication)),
    path('profile/', include(profile)),
]
