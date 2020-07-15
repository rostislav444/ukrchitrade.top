from django.db import models
from ckeditor.fields import RichTextField
from apps.core.models import OneImage, OneFile, NameSlug, Images
from django.utils.text import slugify
import unidecode
from django.core import exceptions
from docxtpl import DocxTemplate
from django.utils.timezone import now


class Category(NameSlug):
    # Bool
    ignore_multiply = models.BooleanField(default=False, verbose_name='Игнорировать мультипликатор цены')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ProductType(NameSlug):
    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

# Product
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, verbose_name='Тип')
    code = models.CharField(max_length=255, verbose_name='Код')
    customs_code = models.CharField(blank=True, max_length=255, verbose_name='УКТЗЕД')
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    slug = models.SlugField(blank=True, max_length=255, verbose_name='Идентификатор')
    price =     models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена') 
    price_old = models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена старая') 
    price_box = models.BooleanField(default=False, verbose_name='Цена за ящик')
    manufacturer = models.CharField(blank=True, max_length=255, verbose_name='Производитель')
    delivery_time = models.DateField(blank=True, null=True, verbose_name='Время поставки')
    # Standarts
    stnadrt_eu = models.CharField(blank=True, default='', max_length=255)
    stnadrt_us = models.CharField(blank=True, default='', max_length=255)
    stnadrt_cn = models.CharField(blank=True, default='', max_length=255)
    # Box
    box_w = models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='W, см') 
    box_l = models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='L, см') 
    box_h = models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='H, см') 
    volume = models.DecimalField(default=0, decimal_places=4, max_digits=200, verbose_name='Обьем')
    weight_netto = models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Вес, нетто')
    weight_brutto = models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Вес, брутто')
    volume_weight = models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Обьемный вес')
    pieces_in_box = models.PositiveIntegerField(default=1, verbose_name='Шт. в ящике') 
    pieces_in_pack = models.PositiveIntegerField(default=1, verbose_name='Шт. в упаковке') 
    # Text
    description = RichTextField(blank=True, verbose_name='Описание')
    short_description = models.TextField(blank=True, verbose_name='Короткое описание')
    notes = models.CharField(blank=True, max_length=255, verbose_name='Примечания')
    update = models.DateTimeField(default=now)
    
    class Meta:
        ordering = ['category',]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return ' - '.join([self.code, self.name])

    def save(self):
        self.update = now
        if self.price != self.price_old:
            print('Price changed')
        self.price == self.price_old
        super(Product, self).save()

    @property
    def get_category(self):
        return str(self.category.name)

    @property
    def get_type(self):
        return self.product_type.name

    @property
    def box_price(self):
        if self.price_box:
            return self.price
        return self.price * self.pieces_in_box

    @property
    def get_delivery_time(self):
        date = self.delivery_time
        if date is not None:
            print(self.delivery_time.__dir__())
            return self.delivery_time.strftime("%d/%m/%Y")
        return '-'

    @property
    def get_volume(self):
        volume = self.box_w * self.box_l * self.box_h / 1000 / 1000
        return round(volume, 4)

    @property
    def get_volume_weight(self):
        volume_weight = self.get_volume * 167
        return round(volume_weight, 2)
    
    @property
    def air_delivery_pc(self):
        weight = self.volume_weight
        if self.weight_netto > self.volume_weight:
            weight = self.weight_netto
        return weight / self.pieces_in_box * 10

    @property
    def air_delivery_pc_price(self):
        return self.air_delivery_pc + self.price 

    @property
    def air_delivery_box(self):
        return self.air_delivery_box * self.pieces_in_box

    @property
    def air_delivery_box_price(self):
        return (self.air_delivery_pc + self.price) * self.pieces_in_box
    
   
    def translate(self):
        return ''




class ProductImages(Images):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        ordering = ['-num']
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
    

class ProductDocuments(OneFile):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="documents")

    class Meta:
        ordering = ['-num']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
    

class ProductPresentation(OneFile):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="presentations")

    class Meta:
        ordering = ['-num']
        verbose_name = 'Презентация'
        verbose_name_plural = 'Презентации'
    

class ProductCertificate(OneFile):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="certificates")

    class Meta:
        ordering = ['-num']
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
    




