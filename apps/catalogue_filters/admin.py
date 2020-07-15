from django.contrib import admin
from django import forms
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ObjectDoesNotExist
from django.urls import resolve
from .models import *
from django.contrib.admin.widgets import FilteredSelectMultiple
from apps.catalogue.admin import ProductAdmin
from apps.catalogue.models import Product
from django.forms.models import inlineformset_factory


# ATTRIBUTE
class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 0

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeValueInline
    ]


# ATTRIBUTE VALUE
@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    pass


# CATEGORY ATTRIBUTE

class CategoryAttributeValueInline(admin.TabularInline):
    model = CategoryAttributeValue
    extra = 0


class CategoryAttributeAdminForm(forms.ModelForm):
    values = forms.ModelMultipleChoiceField(required = False, queryset=AttributeValue.objects.none(), widget = FilteredSelectMultiple(verbose_name='values', is_stacked=False))

    class Meta:
        model = CategoryAttribute
        fields = ('parent','attribute','values')

    def __init__(self, *args, **kwargs):
        super(CategoryAttributeAdminForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs.keys() and kwargs['instance'] is not None:
            self.fields['values'].queryset = AttributeValue.objects.filter(parent = kwargs['instance'].attribute)
       
    def save(self, commit=True):
        return super(CategoryAttributeAdminForm, self).save(commit=commit)


@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):
    obj = None
    form = CategoryAttributeAdminForm
    inlines = [CategoryAttributeValueInline]
    

   
# CATEGORY ATTRIBUTE VALUE
@admin.register(CategoryAttributeValue)
class CategoryAttributeValueAdmin(admin.ModelAdmin):
    pass
   

# PRODUCT ATTRIBUTE
class ProductAttributesForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'value']
        
    def __init__(self, *args, **kwargs):
        super(ProductAttributesForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs.keys():
            self.fields['attribute'].queryset =  CategoryAttribute.objects.filter(pk=kwargs['initial']['attribute'])
            self.fields['value'].queryset = kwargs['initial']['values']
        if 'instance' in kwargs.keys():
            self.fields['attribute'].queryset =  CategoryAttribute.objects.filter(pk=kwargs['instance'].attribute.pk)
            self.fields['value'].queryset = kwargs['instance'].attribute.get_attributes_values


class ProductAttributesFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        if kwargs['instance'].pk:
            product = Product.objects.get(pk=kwargs['instance'].pk)
            exclude = [attr.attribute.pk for attr in product.product_attrs.all()]
            kwargs.update({
                'initial' : [
                    { 'attribute': attribute.pk, 'values' : attribute.get_attributes_values } for attribute in product.category.attributes.exclude(pk__in=exclude)] 
            })
        super(ProductAttributesFormSet, self).__init__(*args, **kwargs)


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    form = ProductAttributesForm
    formset = ProductAttributesFormSet
    fields = ['attribute', 'value']


    def get_max_num(self, request, object=None, **kwargs):
        if object: return len(object.category.attributes.all())
        else: return 0

    def get_extra(self, request, object=None, **kwargs):
        if object: 
            exclude = [attr.attribute.pk for attr in object.product_attrs.all()]
            attrs = object.category.attributes.exclude(pk__in=exclude)
            return len(attrs)
        else: return 0


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    pass


# PRODUCT
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

ProductAdmin.inlines.insert(0, ProductAttributeInline)


