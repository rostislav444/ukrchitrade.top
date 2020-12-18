from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


@admin.register(Incoterms)
class IncotermsAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceFormula)
class PriceFormulaAdmin(admin.ModelAdmin):
    pass

class InvoiceProductsInline(admin.TabularInline):
    model = InvoiceProducts

    def image_preview(self, obj=None):
        if obj.pk:
            img = mark_safe("""<img style="width:240px; height:240px; object-fit: contain; object-position: center; border: 1px solid #ededed;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.product.images.all()[0].image_sq.url, width=240, height=240))
            return img
        else: return '-'


    fields = ['image_preview','invoice','product','quantity','total']
    readonly_fields = ['image_preview','total']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceProductsInline]

    fields = ['code','date','price','incoterms','template','file','total','total_words']
    readonly_fields = ['total','total_words']


@admin.register(InvoiceTemplate)
class InvoiceTemplateAdmin(admin.ModelAdmin):
    pass