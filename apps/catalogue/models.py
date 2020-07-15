from django.core import exceptions
from django.db import models
from django.db.models import Case, When, IntegerField
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from apps.core.models import OneImage, OneFile, NameSlug, Images, Translation
from apps.catalogue_filters.models import *
from project import settings 
import unidecode
from docxtpl import DocxTemplate

import datetime




class Category(NameSlug, Translation):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT)
    # SMALL WHOOSALE
    sm_price = models.DecimalField(default=1.10, decimal_places=2, max_digits=200, verbose_name='Наценка, мелкий опт') 
    sm_start =    models.PositiveIntegerField(blank=True, default=0, verbose_name='Начало малого опта')
    # MIDDLE WHOOSALE
    md_price = models.DecimalField(default=1.05, decimal_places=2, max_digits=200, verbose_name='Наценка, средний опт') 
    md_start =    models.PositiveIntegerField(blank=True, default=0, verbose_name='Начало среднгего опта')
    # BIG WHOOSALE
    bg_price = models.DecimalField(default=1.00, decimal_places=2, max_digits=200, verbose_name='Наценка, крупный опт') 
    bg_start =    models.PositiveIntegerField(blank=True, default=0, verbose_name='Начало большого опта')
    ignore_multiply = models.BooleanField(default=False, verbose_name='Без наценки')
    description = RichTextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ProductType(NameSlug, Translation):
    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

# Product
class ProductModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(has_price=Case(When(price=0, then=0), default=1, output_field=IntegerField()))


class Product(Translation):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Тип')
    code = models.CharField(max_length=255, verbose_name='Код')
    customs_code = models.CharField(blank=True, max_length=255, verbose_name='УКТЗЕД')
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    slug = models.SlugField(blank=True, max_length=255, verbose_name='Идентификатор')
    # PRICE
    price_box =   models.BooleanField(default=False, verbose_name='Цена за ящик')
    # REGULAR PRICE
    price =        models.DecimalField(default=0, decimal_places=4, max_digits=200, verbose_name='Цена')
    price_old =    models.DecimalField(default=0, decimal_places=4, max_digits=200, verbose_name='Старая цена')
    price_update = models.DateTimeField(default=now)
    # SMALL WHOOSALE
    sm_whoosale = models.BooleanField(default=True, verbose_name='Малый опт')
    sm_price =    models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена, мелкий опт') 
    sm_start =    models.PositiveIntegerField(blank=True, default=0, verbose_name='Начало малого опта')
    # MEDIUM WHOOSALE
    md_whoosale = models.BooleanField(default=True, verbose_name='Средний опт')
    md_price =    models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена, средний опт') 
    md_start =    models.PositiveIntegerField(blank=True, default=0, verbose_name='Начало среднгего опта')
    # BIG WHOOSALE
    bg_whoosale = models.BooleanField(default=True, verbose_name='Крупный опт')
    bg_price =    models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена, крупный опт') 
    bg_start =    models.PositiveIntegerField(blank=True, default=0, verbose_name='Начало большого опта')

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

    objects = ProductModelManager()
    
    class Meta:
        ordering = ['category',]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return ' - '.join([self.code, self.name])

    def save(self):
        self.update = datetime.datetime.now()
        if self.price_old != self.price:
            self.price_old = self.price
            self.price_update = datetime.datetime.now()
        super(Product, self).save()


    def get_absolute_url(self):
       return reverse('catalogue:product', kwargs={'id':self.pk})

    @property
    def image(self):
        try: return self.images.all()[0].image_s.url
        except: return '-'

    @property
    def image_full_url(self):
        return settings.MEDIA_ROOT + self.images.first().image_s.name

    # @property
    # def trans(self):
    #     return self

   

    # Documents
    @property
    def has_fda(self):
        length = len(self.certificates.filter(name='FDA'))
        if length > 0: return 'yes'
        return 'no'

    @property
    def has_ce(self):
        length = len(self.certificates.filter(name='CE'))
        if length > 0: return 'yes'
        return 'no'

    @property
    def has_description(self):
        length = len(self.documents.filter(name='DESCRIPTION'))
        if length > 0: return 'yes'
        return 'no'

    @property
    def has_documents(self):
        length = len(self.documents.all())
        if length > 0:
            return 'yes'
        return 'no'


    @property
    def get_category(self):
        return str(self.category.name)

    @property
    def get_type(self):
        try:
            return self.product_type.name
        except:
            return '-'

    @property
    def get_price(self):
        if self.price_box:
            return self.price / self.pieces_in_box
        return round(self.price, 2)

    @property
    def box_price(self):
        if self.price_box:
            return self.price
        return self.price * self.pieces_in_box

    @property
    def get_delivery_time(self):
        date = self.delivery_time
        if date is not None:
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
    def weight_delivery(self):
        volume = self.get_volume_weight
        netto = self.weight_netto
       
        if float(netto) != 0 and float(netto) * 1.5 < float(volume):
            weight = float(netto) * 1.5
        elif netto > volume:
            weight = netto
        else:
            weight = volume
        return round(weight, 4)

 

    @property
    def weight_delivery_pc(self):
        weight = self.weight_delivery
        if self.price_box == False:
            if self.pieces_in_box > 1:
                weight = round(weight / self.pieces_in_box, 4)
            else:
                weight = 0
        return weight
    
    
    @property
    def air_delivery_pc(self):
        if self.price_box == False and self.pieces_in_box < 2:
            value = 0
        else:
            weight = self.get_volume_weight
            if self.weight_netto > self.volume_weight:
                weight = self.weight_netto
            value = round(weight / self.pieces_in_box * 12, 2)
        return value

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

    # START QUANTITY
    @property
    def get_sm_start(self):
        if self.pieces_in_box > 1:
            return self.pieces_in_box
        return self.category.sm_start

    @property
    def get_md_start(self):
        if self.md_start: return self.md_start
        return self.category.md_start

    @property
    def get_bg_start(self):
        if self.bg_start: return self.bg_start
        return self.category.bg_start

    # START PRICE
    @property
    def get_sm_price(self):
        price =  self.price
        price = float(price) * float(self.category.sm_price)
        if self.price_box:
            price = price / float(self.pieces_in_box)
        return round(float(price), 4)

    
    @property
    def get_md_price(self):
        price =  self.price
        price = float(price) * float(self.category.md_price)
        if self.price_box:
            price = price / float(self.pieces_in_box)
        return round(float(price), 4)

    @property
    def get_bg_price(self):
        price =  self.price
        price = float(price) * float(self.category.bg_price) 
        if self.price_box:
            price = price / float(self.pieces_in_box)
        return round(float(price), 4)






class ProductImages(Images):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        ordering = ['-num']
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
    

class ProductCertificate(OneFile):
    CERTIFICATE_TYPE = [
        ('FDA', 'FDA'),
        ('CE', 'CE'),
        ('CHI', 'CHI'),
    ]

    name =    models.CharField(max_length=100, blank=False, choices=CERTIFICATE_TYPE, verbose_name="Тип сертфиката")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="certificates")

    class Meta:
        ordering = ['-num']
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def update_product_attrs(self):
        # ATTR GROUP
        try: attr = Attribute.objects.get(name="Сертификат")
        except: 
            attr = Attribute(name="Сертификат")
            attr.save()
        # ATTR VALUE
        attr_values = []
        for certificate_name in set(self.product.certificates.all().values_list('name', flat=True)):
            # ATTR VALUE
            try: value = AttributeValue.objects.get(parent=attr, name=certificate_name)
            except: 
                value = AttributeValue(parent=attr, name=certificate_name)
                value.save()
            print(value)
            # if value.name == self.name:
            attr_values.append(value)
        print( attr_values)
                
        # CATEGORY ATTR GROUP
        try: cat_attr = CategoryAttribute.objects.get(parent=self.product.category, attribute=attr)
        except:
            cat_attr = CategoryAttribute(parent=self.product.category, attribute=attr)
            cat_attr.save()
        cat_attr.values.add(*attr.values.all())
        super(CategoryAttribute, cat_attr).save()
        # CATEGORY ATTR VALUE
        try: prod_attr_val = ProductAttribute.objects.get(parent=self.product, attribute=cat_attr)
        except: 
            prod_attr_val = ProductAttribute(parent=self.product, attribute=cat_attr)
            prod_attr_val.save()
        prod_attr_val.value.set(attr_values)
        super(ProductAttribute, prod_attr_val).save()


    def save(self):
        super(ProductCertificate, self).save()
        self.update_product_attrs()

    def delete(self):
        super(ProductCertificate, self).delete()
        self.update_product_attrs()
        
    
        
        


class ProductDocuments(OneFile, Translation):
    CERTIFICATE_TYPE = [
        ('DESCRIPTION',  'Описание'),
        ('PRESENTATION', 'Презентация'),
        ('METHOD',       'Способ применения'),

    ]

    name =    models.CharField(max_length=100, blank=False, choices=CERTIFICATE_TYPE, verbose_name="Тип документа")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="documents")

    class Meta:
        ordering = ['-num']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
    

class ProductPriceHistory(models.Model):
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price =  models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена')
    update = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-update']
        verbose_name = 'История цен'
        verbose_name_plural = 'История цен'
    




