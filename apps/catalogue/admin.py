from django.contrib import admin
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms import TextInput, Textarea
from apps.core.admin_globals import InlineObjectLink, AdminImagePreview
from apps.catalogue_filters.models import CategoryAttribute
from .models import *


FORMFIELD_OVERRIDES = {
    models.PositiveIntegerField: {'widget': TextInput(attrs={'size':'30'})},
    models.CharField: {'widget': TextInput(attrs={'size':'30'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':61})},
}

class CategoryAttributeinline(admin.TabularInline, InlineObjectLink):
    readonly_fields = ['link']
    fields = ['attribute','link']
    model = CategoryAttribute
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryAttributeinline,]
    list_display = ['name','sm_price','md_price','bg_price']
    list_editable = ['sm_price','md_price','bg_price']
    formfield_overrides = FORMFIELD_OVERRIDES



@admin.register(ProductDocuments)
class ProductDocumentsAdmin(admin.ModelAdmin): pass


class ProductImagesInline(admin.TabularInline, AdminImagePreview):
    model = ProductImages
    readonly_fields = ['image_preview']
    extra = 0
    fieldsets = (
        ('Цена', {'fields': ('num', 'image_preview', 'image')}),
    )


class ProductCharacteristicsInline(admin.TabularInline):
    model = ProductCharacteristics
    extra = 1


class ProductDocumentsInline(admin.TabularInline):
    model = ProductDocuments
    extra = 1


class ProductCertificateInline(admin.TabularInline):
    model = ProductCertificate
    extra = 1





@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def image_preview(self, obj=None):
        try:
            img = mark_safe("""
            <img style="border-radius:4px;width:120px; height:120px; object-fit: cover; object-position: center; border: 1px solid #ededed;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.images.all()[0].image_xs.url, width=120, height=120))
            return img
        except: return '-'
    image_preview.short_description = 'Фото'

    readonly_fields = [
        'image_preview',
        'volume','volume_weight',
        'get_sm_price','get_md_price','get_bg_price'
    ]
    list_display = [
        'image_preview','code','name','sm_price','price','category',
        'manufacturer','weight_netto','weight_brutto','volume',
        'volume_weight', 'customs_code']
    list_filter = ['category', 'price']
    list_editable = ['price','sm_price']
    inlines = [
        ProductImagesInline, ProductCharacteristicsInline, ProductDocumentsInline, ProductCertificateInline
    ]
    fieldsets = (
        ('Продукт', 
            {'fields': (
                ('image_preview','translate_childs'),
                'category','manufacturer',
                'code','customs_code','name')}
        ),
        ('Входная цена', {'fields': ('entry_price',),}),
        ('Розничная цена', {'fields': (
            ('price','price_old'),
            ('price_ua','price_old_ua'),
            'price_box'),
        }),
        ('Малый опт',   {'fields': (('sm_price', 'sm_start', 'get_sm_price','sm_whoosale'),'sm_price_ua')}),
        ('Средний опт', {'fields': (('md_price', 'md_start', 'get_md_price','md_whoosale'),'md_price_ua')}),
        ('Крупный опт', {'fields': (('bg_price', 'bg_start', 'get_bg_price','bg_whoosale'),'bg_price_ua')}),
       
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
