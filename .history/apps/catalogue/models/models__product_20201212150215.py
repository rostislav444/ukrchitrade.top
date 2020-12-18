from django.core import exceptions
from django.db import models
from django.db.models import Case, When, IntegerField
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from apps.core.models import NameSlug, Translation
from apps.core.models.models__file import OneFile
from apps.core.models.models__images import ModelImages, Image
from apps.catalogue_filters.models import *
from project import settings 
from docxtpl import DocxTemplate
import datetime, unidecode



class ProductModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(has_price=Case(When(price=0, then=0), default=1, output_field=IntegerField()))


class Product(NameSlug, Translation):
    category =          models.ForeignKey('catalogue.Category', on_delete=models.PROTECT, blank=False, verbose_name='Категория', related_name='products')
    code =              models.CharField(max_length=255, verbose_name='Код')
    customs_code =      models.CharField(blank=True, max_length=255, verbose_name='УКТЗЕД')
    name =              models.CharField(max_length=255, verbose_name='Название продукта')
    slug =              models.SlugField(blank=True, max_length=255, verbose_name='Идентификатор')
    # PRICE
    price_box =         models.BooleanField(default=False, verbose_name='Цена за ящик')
    
    # ENTRY PRICE
    entry_price =       models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Входная цена')
    # RETAIL
    price =             models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Розничная цена')

    price_ua =          models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Розничная цена UA')
    price_old =         models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Старая розничная цена')
    price_old_ua =      models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Старая розничная цена UA')
    # SMALL WHOOSALE
    sm_whoosale =       models.BooleanField(default=True, verbose_name='Малый опт')
    sm_price =          models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена, мелкий опт') 
    sm_price_ua =       models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена, мелкий опт UA') 
    sm_start =          models.PositiveIntegerField(blank=True, default=0, verbose_name='Начало малого опта')
    # MEDIUM WHOOSALE
    md_whoosale =       models.BooleanField(default=True, verbose_name='Средний опт')
    md_price =          models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена, средний опт') 
    md_price_ua =       models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена, средний опт UA') 
    md_start =          models.PositiveIntegerField(blank=True, default=0, verbose_name='Начало среднгего опта')
    # BIG WHOOSALE
    bg_whoosale =       models.BooleanField(default=True, verbose_name='Крупный опт')
    bg_price =          models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена, крупный опт') 
    bg_price_ua =       models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Цена, крупный опт UA') 
    bg_start =          models.PositiveIntegerField(blank=True, default=0, verbose_name='Начало большого опта')
    manufacturer =      models.CharField(blank=True, max_length=255, verbose_name='Производитель')
   
    # Box
    box_w =             models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='W, см') 
    box_l =             models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='L, см') 
    box_h =             models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='H, см') 
    volume =            models.DecimalField(default=0, decimal_places=4, max_digits=200, verbose_name='Обьем')
    weight_netto =      models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Вес, нетто')
    weight_brutto =     models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Вес, брутто')
    volume_weight =     models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Обьемный вес')
    pieces_in_box =     models.PositiveIntegerField(default=1, verbose_name='Шт. в ящике') 
    pieces_in_pack =    models.PositiveIntegerField(default=1, verbose_name='Шт. в упаковке') 
    # Text
    description =       RichTextField(blank=True, verbose_name='Описание')
    short_description = models.TextField(blank=True, verbose_name='Короткое описание')
    notes =             models.CharField(blank=True, max_length=255, verbose_name='Примечания')
    create =            models.DateTimeField(default=now)
    update =            models.DateTimeField(default=now)
    price_update =      models.DateTimeField(default=now)
    view =              models.PositiveIntegerField(default=0)
    objects =           ProductModelManager()
    

    class Meta:
        ordering = ['category',]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return ' - '.join([self.code, self.name])

    def save(self):
        self.set_prices()
        self.set_whoosale_start()
        self.update = datetime.datetime.now()
        super(Product, self).save()

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={
            'category' : self.category.slug,
            'slug' : self.slug,
            'product_id' : self.pk
        })

    def get_databse_url(self):
        return reverse('catalogue:product', kwargs={'id':self.pk})

    @property
    def get_image(self):
        image = self.images.first()
        print('IMAGE',image)
        if image:
            try: return image.image_thmb['l']['path']
            except: pass
        return 'static/img/no_image.png'


    def set_whoosale_start(self):
        levels = ['sm','md','bg']
        for level in levels:
            level = level + '_start'
            start = getattr(self.category, level)
            if getattr(self, level) == 0:
                setattr(self, level, start)

   
    def set_prices(self):
        # Set retail price and whoosale prices from the entry price, multiplied by
        # product category murckup koeficient.
        levels = ['price','sm_price','md_price','bg_price']
        if self.entry_price:
            entry = self.entry_price
            for price_level in levels:
                price = float(entry) * float(getattr(self.category, price_level))
                if self.price_box:
                    price = price / float(self.pieces_in_box)
                setattr(self, price_level, round(float(price), 4))
                setattr(self, price_level + '_ua', round(float(price * 28), 4))
       
        

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


    def pricePretyfier(self, price):
        if self.price_box: 
            price = price / self.pieces_in_box
        if int(price) == price: 
            return int(price)
        return round(price, 2)

    @property
    def get_price(self): return self.pricePretyfier(self.price)

    @property
    def get_price_ua(self): return self.pricePretyfier(self.price_ua)

    @property
    def get_old_price(self): return self.pricePretyfier(self.price_old)

    @property
    def get_old_price_ua(self): return self.pricePretyfier(self.price_old_ua)



    @property
    def box_price(self):
        if self.price_box:
            return self.price
        return self.price * self.pieces_in_box

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
        price = self.entry_price
        price = float(price) * float(self.category.sm_price)
        if self.price_box:
            price = price / float(self.pieces_in_box)
        return round(float(price), 4)

    @property
    def get_md_price(self):
        price = self.entry_price
        price = float(price) * float(self.category.md_price)
        if self.price_box:
            price = price / float(self.pieces_in_box)
        return round(float(price), 4)

    @property
    def get_bg_price(self):
        price = self.entry_price
        price = float(price) * float(self.category.bg_price) 
        if self.price_box:
            price = price / float(self.pieces_in_box)
        return round(float(price), 4)

    def all_prices(self):
        price_lvls = ['bg','md','sm','retail']
        for n, lvl in enumerate(price_lvls):
            price_lvls[n] = {'key' : lvl, 'start' : getattr(self, lvl + '_start'), 'price' :  getattr(self, lvl + '_price_ua')}
        return price_lvls
            
    def get_quantity_price(self, quantity):
        for lvl in ['bg','md','sm']:
            start = getattr(self, lvl + '_start')
            price = getattr(self, lvl + '_price_ua')
            if quantity >= start:
                return round(float(price),2)
        return round(float(self.price_ua),2)
        



class ProductImages(Image):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        ordering = ['-num']
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'


class ProductCharacteristics(models.Model):
    num =          models.PositiveIntegerField(default=0)
    parent =       models.ForeignKey(Product, on_delete=models.CASCADE, related_name="characteristics")
    name =         models.CharField(max_length=255)
    description =  models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-num']
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
    

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
    


    




