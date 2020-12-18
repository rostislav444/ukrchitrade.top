from django.db import models
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
import jsonfield


# GLOBALS
FORMFIELD_OVERRIDES = {
    models.CharField: {'widget': TextInput(attrs={'size':'50'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':61})},
    jsonfield.JSONField: {'widget': Textarea(attrs={'rows':4, 'cols':61})},
}


class ParentAdminRedirect(admin.ModelAdmin):
    class Meta:
        abstract = True

    def response_add(self, request, obj, post_url_continue=None):
        if "_continue" not in request.POST:
            obj = obj.parent
        return redirect(reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)]))

    def response_change(self, request, obj):
        if "_continue" not in request.POST:
            obj = obj.parent
        return redirect(reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)]))


class ObjectParentLink():
    def __init__(self, *args, **kwargs):
        parent_link = self.parent_link
        super(ObjectParentLink, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    def parent_link(self, obj=None):
        url = reverse('admin:%s_%s_change' % (obj.parent._meta.app_label, obj.parent._meta.model_name), args=[force_text(obj.parent.pk)])
        url = f'''<a href="{url}" style="font-weight: 800; text-transform: uppercase;">{obj.parent}</a>'''
        return mark_safe(url)
    parent_link.short_description = 'Назад'


class InlineObjectLink():
    def __init__(self, *args, **kwargs):
        link = self.link
        super(InlineObjectLink, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    def link(self, obj=None):
        if obj.pk:
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            url = f'''<a href="{url}" style=" display: inline-block; min-width: 240px; margin: 0; border: none; border-radius: 4px; color: black; padding: 4px 8px; background-color: #f6f6f6;  border: 1px solid #adadad;">url: {obj.__str__()}</a>'''
            return mark_safe(url)
        return _("Обьект не создан")


class AdminImagePreview():
    def __init__(self, *args, **kwargs):
        image_preview = self.image_preview 
        super(AdminImagePreview, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    def image_preview(self, obj=None):
        try: url = obj.image_thmb["s"]["path"]
        except: url = "/static/img/no_image.png"
        style = {
            'height' : '120px',
            'width' : '120px',
            'object-fit' : 'contain',
            'object-position' : 'center',
            'box-shadow' : '0 4px 8px rgba(0,0,0,0.15)',
            'margin-right' : '16px', 
            'margin-bottom': '16px',
            'border-radius': '4px',
        }
        style = ';'.join([':'.join([k,v]) for k,v in style.items()])
        html = f'<img style="{style}" src="{url}">'
        return mark_safe(html)

    image_preview.short_description = 'Предпросмотр'
  

