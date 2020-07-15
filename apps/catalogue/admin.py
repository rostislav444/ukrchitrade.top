from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms import TextInput, Textarea

# GLOBALS
FORMFIELD_OVERRIDES = {
    models.PositiveIntegerField: {'widget': TextInput(attrs={'size':'30'})},
    models.CharField: {'widget': TextInput(attrs={'size':'30'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':61})},
}



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name','sm_price','md_price','bg_price'
    ]
    list_editable = ['sm_price','md_price','bg_price']
    formfield_overrides = FORMFIELD_OVERRIDES


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductDocuments)
class ProductDocumentsAdmin(admin.ModelAdmin):
    pass

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    readonly_fields = ['image_preview']
    extra = 1

    def image_preview(self, obj=None):
        if obj.pk:
            img = mark_safe("""<img style="width:240px; height:240px; object-fit: contain; object-position: center; border: 1px solid #ededed;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_sq.url, width=240, height=240))
            return img
        else:
            return '-'

    fields = ['num','image_preview','image_l']

    image_preview.short_description = 'Предпросмотр'




class ProductDocumentsInline(admin.TabularInline):
    model = ProductDocuments
    extra = 1


class ProductCertificateInline(admin.TabularInline):
    model = ProductCertificate
    extra = 1


class ProductPriceHistoryInline(admin.TabularInline):
    model = ProductPriceHistory
    extra = 0



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['volume','volume_weight', 'get_sm_price', 'get_md_price', 'get_bg_price']
    list_display = [
        'image_preview','code','name','sm_price','price','category',
        'manufacturer','weight_netto','weight_brutto','volume',
        'volume_weight', 'customs_code']
    list_filter = ['category', 'price']
    list_editable = ['price','sm_price']

    def image_preview(self, obj=None):
        try:
            img = mark_safe("""
            <img style="border-radius:4px;width:80px; height:80px; object-fit: contain; object-position: center; border: 1px solid #ededed;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.images.all()[0].image_xs.url, width=120, height=120))
            return img
        except:
            return '-'

    inlines = [
        ProductImagesInline, ProductDocumentsInline, 
        ProductCertificateInline, ProductPriceHistoryInline
    ]
    fieldsets = (
        ('Продукт', 
            {'fields': (
                'translate_childs','category','product_type','manufacturer',
                'code','customs_code','name','delivery_time')}
        ),
        ('Цена', {'fields': ('price','price_box')}),
        ('Малый опт',   {'fields': (('sm_price', 'sm_start', 'get_sm_price','sm_whoosale'),)}),
        ('Средний опт', {'fields': (('md_price', 'md_start', 'get_md_price','md_whoosale'),)}),
        ('Крупный опт', {'fields': (('bg_price', 'bg_start', 'get_bg_price','bg_whoosale'),)}),
        ('Стандарты', 
            {'fields': (
                'stnadrt_eu','stnadrt_us','stnadrt_cn')}
        ),
        ('Коробка', 
            {'fields': (
                ('box_w','box_l','box_h'),
                ('pieces_in_pack','pieces_in_box'),
                'weight_netto','weight_brutto')}
        ),
        ('Текст', 
            {'fields': ('description','notes')}
        ),
    )
