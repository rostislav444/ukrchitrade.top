from django.urls import include, path, re_path
from django.views.generic import TemplateView
from apps.search import views


app_name = "search"


urlpatterns = [
    path('', views.SearchView.as_view(), name="search")
]