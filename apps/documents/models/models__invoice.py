from django.db import models
from apps.core.models import OneFile, Languages, TranslatorsTranslate
from apps.catalogue.models import Product, Category
from django.core import exceptions
from apps.core.models import NameSlug
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from io import BytesIO
from project import settings 
from django.utils.text import slugify
from unidecode import unidecode
from num2words import num2words
import os
import jinja2
from decimal import Decimal



def priceFormulaValidator(value):
    value = value.replace(' ','')
    err_val = []
    for i in value:
        if i not in 'x/*+-.0123456789':
            err_val.append(i)
    if len(err_val) > 0:
        raise exceptions.ValidationError(f'Формула имеет не допустимые значения: {str(err_val)}')

    x = 1
    try:
        eval(value)
    except:
        raise exceptions.ValidationError(f'Формула не валидна')


# Invoice
class PriceFormula(models.Model):
    formula = models.CharField(max_length=255, verbose_name='Формула подсчета', help_text='Цену подставлять в виде английского "x"', validators=[priceFormulaValidator])

    class Meta:
        ordering = ['formula']
        verbose_name = 'Формула цены'
        verbose_name_plural = 'Формулы цен'

    def __str__(self):
        return self.formula

    def calc(self, price):
        x = float(price)
        return round(eval(self.formula), 4)

    def save(self):
        x = 2
        y = eval(self.formula)
        super(PriceFormula, self).save()



class Incoterms(NameSlug):
    price =  models.DecimalField(default=10, decimal_places=2, max_digits=200, verbose_name='Ставка перевозчика')
    formula = models.CharField(max_length=255, verbose_name='Формула подсчета', help_text='Цену подставлять в виде английского "x"', validators=[priceFormulaValidator])

    class Meta:
        ordering = ['name']
        verbose_name = 'Инкотермс'
        verbose_name_plural = 'Инкотермс'

    def calc(self):
        return ''

    def air(self):
        self.price
        return 0



class InvoiceTemplate(OneFile):
    class Meta:
        verbose_name = 'Шаблон инвойса'
        verbose_name_plural = 'Шаблоны инвойсов'

    def __str__(self):
        return f'{self.name}'


class Invoice(models.Model):
    code =      models.CharField(max_length=255, unique=True, verbose_name='Код')
    date =      models.DateField(verbose_name='Дата')
    price =     models.ForeignKey('documents.PriceFormula', on_delete=models.PROTECT)
    incoterms = models.ForeignKey(Incoterms, blank=True, null=True, on_delete=models.PROTECT, related_name="incoterms")
    template =  models.ForeignKey(InvoiceTemplate, on_delete=models.PROTECT, verbose_name='Шаблон')
    file =      models.FileField(blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Инвойс'
        verbose_name_plural = 'Инвойсы'

    def __str__(self):
        return f'{self.code}, {self.date}'
        
    @property
    def total(self):
        total = 0
        for product in self.products.all():
            total += product.total
        return round(float(total), 2)

    @property
    def total_with_delivery(self):
        total = 0
        for product in self.products.all():
            total += product.total_with_delivery
        return round(float(total), 2)



    @property
    def total_qty(self):
        quantity = 0
        for product in self.products.all():
            quantity += product.quantity
        return quantity

    @property
    def total_words(self):
        return str(num2words(self.total, lang='en'))

    @property
    def total_words_ru(self):
        return str(num2words(self.total, lang='ru'))
        
    @property
    def total_words_ua(self):
        text = str(num2words(self.total, lang='ru'))
        return TranslatorsTranslate(text, 'uk')

    @property
    def gross_weight_brutto(self):
        weight = 0
        for product in self.products.all():
            weight += product.weight_brutto
        return round(weight, 4)

    @property
    def gross_weight_netto(self):
        weight = 0
        for product in self.products.all():
            weight += product.weight_netto
        return round(weight, 4)

    @property
    def cartoon_size(self):
        sizes = {'w':0, 'h':0, 'l':0}
        for product in self.products.all():
            qty = float(product.quantity) / float(product.product.pieces_in_box)
            sizes['w'] += float(product.product.box_w) * float(qty)
            sizes['h'] += float(product.product.box_h) * float(qty)
            sizes['l'] += float(product.product.box_l) * float(qty)
        sizes['w'] = round(sizes['w'],2)
        sizes['h'] = round(sizes['h'],2)
        sizes['l'] = round(sizes['l'],2)
        return sizes
        

    def generate(self):
        template = self.template.file._get_file()
        doc = DocxTemplate(template)
        invoiceProducts = self.products.all()
        products__pk = [product.product.pk for product in invoiceProducts]

        if len(invoiceProducts) == 0:
            categories = Category.objects.all()
        else:
            categories = Category.objects.distinct().filter(products__pk__in=products__pk)
            



        for category in categories:
            if len(products__pk) > 0:
                category.products_all = category.products.filter(pk__in=products__pk) 
            else:
                category.products_all = category.products.all()
            for product in category.products_all:
                product.img = InlineImage(doc, product.image_full_url, width=Mm(32), height=Mm(32))
                delivery = round(float(product.weight_delivery_pc) * float(self.incoterms.price), 2)
                # SM
                if category.ignore_multiply:
                    sm_price = product.get_sm_price
                else: sm_price = self.price.calc(product.get_sm_price)
                
                product.sm_price =     round(sm_price, 2)
                product.sm_price_uah = round(sm_price * 26.6, 2)
                if delivery > 0:
                    sm_delivery = float(sm_price) + delivery
                    product.sm_delivery =     round(sm_delivery, 2)
                    product.sm_delivery_uah = round(sm_delivery * 26.6, 2)
                else:
                    product.sm_delivery = '-'
                    product.sm_delivery_uah = '-'
                # MD
                if category.ignore_multiply:
                    md_price = product.get_md_price
                else: md_price = self.price.calc(product.get_md_price)

                product.md_price =     round(md_price, 2)
                product.md_price_uah = round(md_price * 26.6, 2)
                if delivery > 0:
                    md_delivery = float(md_price) + delivery
                    product.md_delivery =     round(md_delivery, 2)
                    product.md_delivery_uah = round(md_delivery * 26.6, 2)
                else:
                    product.md_delivery = '-'
                    product.md_delivery_uah = '-'

                # BG 
                if category.ignore_multiply:
                    bg_price = product.get_bg_price
                else: bg_price = self.price.calc(product.get_bg_price)

                product.bg_price =     round(bg_price, 2)
                product.bg_price_uah = round(bg_price * 26.6, 2)
                if delivery > 0:
                    bg_delivery = float(bg_price) + delivery
                    product.bg_delivery =  round(bg_delivery, 2)
                    product.bg_delivery_uah = round(bg_delivery * 26.6, 2)
                else:
                    product.bg_delivery = '-'
                    product.bg_delivery_uah = '-'
        


        for product in invoiceProducts:
            product.img = InlineImage(doc, product.image_full_url, width=Mm(24), height=Mm(24))
            
        
        context = { 
            'invoice' : self,
            'products' : invoiceProducts,
            'exporter' : self.exporter,
            'importer' : self.importer,
            'categories' : categories,
        }

        jinja_env = jinja2.Environment(autoescape=True)
        doc.render(context, jinja_env)

        # name = unidecode('-'.join(['invoice',self.code, str(self.date), 'id', str(self.pk)]))

       
        formula = ''.join(x for x in self.price.formula if x.isdigit())
        if len(formula) == 0:
            formula = 0

        name = f"presentation_en_{str(int(formula))}_{str(int(self.incoterms.price))}"
     
        filename = f'Invoices/{name}.docx'
        doc.save(settings.MEDIA_ROOT + filename)
        self.file.name = filename
        self.save()
        # try: os.remove(settings.MEDIA_ROOT + filename)
        # except: pass
        return settings.MEDIA_URL + filename
    


class InvoiceProducts(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('catalogue.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0, verbose_name='Колличество')

    class Meta:
        unique_together = ('invoice', 'product')

    @property
    def image_full_url(self):
        return settings.MEDIA_ROOT + self.product.images.first().image_xs.name

    @property
    def image(self):
        return self.product.images.first().image_xs.url

    @property
    def price(self):
        price = self.product.price
        quantity = self.quantity
        if   int(quantity) >= int(self.product.get_bg_start): price = self.product.get_bg_price
        elif int(quantity) >= int(self.product.get_md_start): price = self.product.get_md_price
        elif int(quantity) <= int(self.product.get_sm_start): price = self.product.get_sm_price
        x = float(price)
        x = float(eval(self.invoice.price.formula))
        return round(x, 4)

    @property
    def total(self):
        total = float(self.price) * int(self.quantity)
        return round(total,2)

    @property
    def price_with_delivery(self):
        price = float(self.price) +  float(self.product.air_delivery_pc)
        return round(price, 4)

    @property
    def total_with_delivery(self):
        total = float(self.price_with_delivery) * int(self.quantity)
        return round(total,2)

    @property
    def weight_brutto(self):
        weight = float(self.quantity) * float(self.product.weight_brutto) / float(self.product.pieces_in_box)
        return round(weight, 2)

    @property
    def weight_netto(self):
        weight = float(self.quantity) * float(self.product.weight_netto) / float(self.product.pieces_in_box)
        return round(weight, 2)


    
        

    def save(self):
        super(InvoiceProducts, self).save()