from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, path, include
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('apps.catalogue.urls')),
    path('documents', include('apps.documents.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api-auth/', include('rest_framework.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()