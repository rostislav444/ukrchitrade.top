from django.contrib import admin
from django import forms
from .models import *






class CurrencyExchageInline(admin.TabularInline):
    model = CurrencyExchage
    fk_name = 'parent'
    readonly_fields = ['currency','value','date']
    extra = 0

    def get_max_num(self, request, instance=None, **kwargs):
        if instance: 
            if instance.base:
                return CurrencyExchage.objects.filter(parent=instance).count()
        return 0
            

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    def cource(self, obj):
        if obj.pk:
            try:
                c = CurrencyExchage.objects.get(pk=obj.pk)
                return c.value
            except: pass
        return '-'
    cource.short_description = 'Курс'
    readonly_fields = ['cource']
    inlines = [CurrencyExchageInline]
    list_display = [
        'name', 'cource', 'code', 'base'
    ]