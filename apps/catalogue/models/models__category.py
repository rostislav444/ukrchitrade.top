from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.core.models import NameSlug
from apps.catalogue_filters.models import *
from project import settings 
from apps.core.models import Translation
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
import datetime, unidecode



class Category(NameSlug, Translation, MPTTModel):
    parent =        TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # RETAIL
    price =         models.DecimalField(default=1.25, decimal_places=2, max_digits=200, verbose_name='Наценка, розница') 
    # SMALL WHOOSALE
    sm_price =      models.DecimalField(default=1.10, decimal_places=2, max_digits=200, verbose_name='Наценка, мелкий опт') 
    sm_start =      models.PositiveIntegerField(blank=True, default=10, verbose_name='Начало малого опта')
    # MIDDLE WHOOSALE
    md_price =      models.DecimalField(default=1.05, decimal_places=2, max_digits=200, verbose_name='Наценка, средний опт') 
    md_start =      models.PositiveIntegerField(blank=True, default=20, verbose_name='Начало среднгего опта')
    # BIG WHOOSALE
    bg_price =      models.DecimalField(default=1.00, decimal_places=2, max_digits=200, verbose_name='Наценка, крупный опт') 
    bg_start =      models.PositiveIntegerField(blank=True, default=40, verbose_name='Начало большого опта')
    ignore_multiply = models.BooleanField(default=False, verbose_name='Без наценки')
    description = RichTextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_slug(self):
        slug = slugify(unidecode.unidecode(self.name))
        return slug

    @property
    def products_count(self):
        from apps.catalogue.models.models__product import Product
        return Product.objects.filter(category__in=self.get_descendants(include_self=True)).distinct().count()

    def get_absolute_url(self):
        return reverse('shop:catalogue', kwargs={'category' : self.slug})