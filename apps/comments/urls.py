from django.urls import include, path, re_path
from apps.comments import views

app_name = 'comments'

urlpatterns = [
    path('comments/<product_id>/', views.comments, name='comments'),
    re_path(r'^like/(?P<product_id>[0-9]+)/(?P<comment_id>[0-9]+)/(?P<like>like|dislike)$', views.comment_likes, name='like'),
   
]
