from project import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.utils.translation import gettext as _
from django.db import connection
from django.utils.text import slugify
from django.db.models import Q, Prefetch, Case, When, IntegerField,  Count
# APPS
from apps.core.functions.serializer import getSerializerLabels
from apps.catalogue_filters.models import (
    Attribute, AttributeValue, CategoryAttribute, CategoryAttributeValue, ProductAttribute,
)
from apps.catalogue.models import Product, Category
from apps.catalogue.serilaizers import (
    CategorySerializer, AttributeSerializer, AttributeValueSerializer, ProductSerializer,
)
from apps.documents.models import PriceFormula, Invoice, InvoiceTemplate
from apps.financials.models import Company
from apps.documents.serializers import InvoiceSerializer
# Django rest framework
from rest_framework import routers, serializers, viewsets
from rest_framework.fields import SerializerMethodField
from django.views.decorators.csrf import csrf_exempt
# libs
from io import BytesIO
from decimal import *
from unidecode import unidecode
from django.template.defaultfilters import slugify
from datetime import datetime
from django.utils.translation import get_language as lang

#  glob Libs
import json, io, xlsxwriter, zipfile, os



@csrf_exempt
def catalogue(request, *args, **kwargs):
    filters = ['categories', 'atributes']
    params = {}
    for fltr in filters:
        value = request.GET.get(fltr)
        if value != None and len(value) > 0:
            params[fltr] = [int(pk) for pk in value.split(',')]
        else: params[fltr] = []

    # Categories
    categoryQP = {}
    if params['categories']:
        categoryQP['pk__in'] = params['categories']
    categories = Category.objects.filter(**categoryQP)

    category = CategorySerializer(categories.first()).data
    

    # Products
    # productQP =  Q()
    # if params['categories']:
    #     productQP |= Q(category__pk__in = params['categories'] )
      
    # if params['atributes']:
    #     atributes = Attribute.objects.distinct().filter(values__in=params['atributes'])
    #     for attr in atributes:
    #         productQP |= Q(
    #             product_attrs__attribute__pk = attr.pk, 
    #             product_attrs__value__pk__in = params['atributes']
    #         )
           
    

    # q_objects = Q() # Create an empty Q object to start with
    # for t in tags:
    #     q_objects |= Q(tags__tag__contains=t) # 'or' the Q objects together


    # Attributes
    attr_values = AttributeValue.objects.distinct().filter(
        category_values__parent__parent__in = categories,
        product_attrs__parent__category__in = categories,
    )
    attrs = Attribute.objects.distinct().filter(values__in=attr_values)

    count = Count('book', filter=Q(book__rating__gt=5))
    
    
    # Serializers
    attrContext = {
        'attr_values' : attr_values,
        'selected' : params['atributes'],
    }

    attributes = json.loads(json.dumps(AttributeSerializer(attrs, many=True, context=attrContext).data))
    
    args = {
        'attributes' : attributes,
        'categories' : Category.objects.all(),
        'formulas' : PriceFormula.objects.all(),
        'invoices' : Invoice.objects.all(),
        'invoice_templates' : InvoiceTemplate.objects.all(),
        'companies' :  Company.objects.all(),
        # 'context' : context
    }

    if 'size' in kwargs.keys():
        args['size'] = kwargs['size']

    if request.method == 'POST':
        products = Product.objects.all()
        if params['categories']:
            products = products.filter(category__pk__in = params['categories'])

        if params['atributes']:
            atributes = Attribute.objects.distinct().filter(values__in=params['atributes'])
            for attr in atributes:
                products = products.distinct().filter(product_attrs__attribute__attribute__pk = attr.pk, product_attrs__value__pk__in = params['atributes'])
        
        # attr_values
        count = Count('product_attrs', filter=Q(product_attrs__parent__pk__in=products.values_list('pk', flat=True)), distinct=True)
        
        for attr in attrs:
            attr.values.annotate(count=count)
            
            # for value in attr.entry_set.all():
            #     print(value)
            # for value in attr.values.all():
            #     print(value.count)
       
            # products = Product.objects.distinct().filter(category__pk__in = params['categories']).order_by('category','-has_price','code')

        productSerializer = ProductSerializer(products, many=True, context={'whoosale' : kwargs['size'] if 'size' in kwargs.keys() else None })
        productsLabels = getSerializerLabels(ProductSerializer())
        products =  json.loads(json.dumps(productSerializer.data))
    
        response = {
            'products' : products,
            'attributes' : attributes,
            'category' : category
            # 'context' : context,
        }
        dump = json.dumps(response)
        return JsonResponse(dump, content_type='application/json', safe=False)
    else:
        return render(request, 'catalogue/catalogue.html', args)

@csrf_exempt
def product(request, id):
    args = {}
    args['product'] = Product.objects.get(pk=id)
    return render(request, 'catalogue/product/product.html', args)



@csrf_exempt
def export_excel(request, *args, **kwargs):
    output = io.BytesIO()
    print(request.GET.get('products'))
    
    if 'products' in request.GET:
        productsIDs = [int(id) for id in request.GET.get('products').split(',')]
        products = Product.objects.filter(pk__in=productsIDs)
    else:
        products = Product.objects.all()
   


    if 'price' in request.GET:
        priceFormula = PriceFormula.objects.get(pk=int(request.GET.get('price'))).formula
    else: priceFormula = 'x'
   
    workbook = xlsxwriter.Workbook(output)
    ws = workbook.add_worksheet()

    priceFormat = {'num_format': '$#,##0.00'}

    data = [
        { 'title' : '№',                                 'width' : 8,  'attr' : 'num'},
        { 'title' : _('Изображение'),                    'width' : 23, 'attr' : 'image'},
        { 'title' : _('Артикул'),                        'width' : 16, 'attr' : 'code'},
        { 'title' : _('Название продукции'),             'width' : 32, 'attr' : 'name'},
        { 'title' : _('Категория'),                      'width' : 32, 'attr' : 'get_category'},
        { 'title' : _('Тип'),                            'width' : 16, 'attr' : 'get_type'},

        # { 'title' : _('Цена'),                           'width' : 16, 'attr' : 'price',        'format' : {'num_format': '$#,##0.00'}},
        
      
        { 'title' : _('Производитель'),                  'width' : 24, 'attr' : 'manufacturer'},
        # { 'title' : _('Время поставки'),                 'width' : 24, 'attr' : 'get_delivery_time','format' : {'num_format': '[$-x-sysdate]dddd, mmmm dd, yyyy'}},
        { 'title' : _('W'),                              'width' : 4,  'attr' : 'box_w'},
        { 'title' : _('L'),                              'width' : 4,  'attr' : 'box_l'},
        { 'title' : _('H'),                              'width' : 4,  'attr' : 'box_h'},
        { 'title' : _('Обьем'),                          'width' : 12, 'attr' : 'get_volume', 'format' : {'num_format': '#,####0.0000'}},
        { 'title' : _('Обьемный вес'),                   'width' : 12, 'attr' : 'get_volume_weight', 'format' : {'num_format': '#,##0.00'}},
        { 'title' : _('Вес брутто'),                     'width' : 12, 'attr' : 'weight_brutto'},
        { 'title' : _('Вес доставки'),                   'width' : 12, 'attr' : 'weight_delivery'},
        { 'title' : _('Штук в ящике'),                   'width' : 12, 'attr' : 'pieces_in_box'},
        
        # { 'title' : _('Цена с доставкой в Киеве, шт'),   'width' : 24, 'value' : '=Q#+F#', 'format' : {'num_format': '$#,##0.00'}},
        # { 'title' : _('Цена с доставкой в Киеве, ящик'), 'width' : 24, 'value' : '=R#*P#', 'format' : {'num_format': '$#,##0.00'}},
        # { 'title' : _('Ссылка на документы'),            'width' : 48, 'attr' : 'link'},
    ] 
    

    if 'whoosale' not in request.GET:
        whoosale = [
            { 'title' : _('Цена'),                           'width' : 16, 'attr' : 'price',        'format' : {'num_format': '$#,##0.00'}},
            { 'title' : _('Мелкий опт'),                     'width' : 16, 'attr' : 'get_sm_price', 'format' : {'bg_color':'deeaff', 'num_format': '$#,##0.00'}},
            { 'title' : _('Цена с доставкой'),               'width' : 16, 'value' : '=H#+Z#',      'format' : {'bg_color':'deeaff', 'num_format': '$#,##0.00'}},
            { 'title' : _('мин. партия'),                    'width' : 16, 'attr' : 'pieces_in_box', 'format' : {'bg_color':'deeaff'}},
            { 'title' : _('Средний опт'),                    'width' : 16, 'attr' : 'get_md_price', 'format' : {'bg_color':'c7dcff', 'num_format': '$#,##0.00'}},
            { 'title' : _('Цена с доставкой'),               'width' : 16, 'value' : '=K#+Z#',      'format' : {'bg_color':'c7dcff', 'num_format': '$#,##0.00'}},
            { 'title' : _('мин. партия'),                    'width' : 16, 'attr' : 'get_md_start', 'format' : {'bg_color':'c7dcff'}},
            { 'title' : _('Крупный опт'),                    'width' : 16, 'attr' : 'get_bg_price', 'format' : {'bg_color':'bdd5ff', 'num_format': '$#,##0.00'}},
            { 'title' : _('Цена с доставкой'),               'width' : 16, 'value' : '=N#+Z#',      'format' : {'bg_color':'bdd5ff', 'num_format': '$#,##0.00'}},
            { 'title' : _('мин. партия'),                    'width' : 16, 'attr' : 'get_bg_start', 'format' : {'bg_color':'bdd5ff'}},
        ]
        delivery = [{ 'title' : _('Цена доставки 1 шт'),      'width' : 24, 'value' : '=X#/Y#*10', 'format' : {'num_format': '$#,##0.00'}}]
       
    else:
        if request.GET.get('whoosale') == 'big':
            whoosale = [
                { 'title' : _('Крупный опт'),                    'width' : 16, 'attr' : 'get_bg_price', 'format' : {'bg_color':'bdd5ff', 'num_format': '$#,##0.00'}},
                { 'title' : _('Цена с достаыкой'),               'width' : 16, 'value' : '=G#+S#',      'format' : {'bg_color':'bdd5ff', 'num_format': '$#,##0.00'}},
                { 'title' : _('мин. партия'),                    'width' : 16, 'attr' : 'get_bg_start', 'format' : {'bg_color':'bdd5ff'}},]
            
        elif request.GET.get('whoosale') == 'middle':
            whoosale = [
                { 'title' : _('Средний опт'),                    'width' : 16, 'attr' : 'get_md_price', 'format' : {'bg_color':'c7dcff', 'num_format': '$#,##0.00'}},
                { 'title' : _('Цена с достаыкой'),               'width' : 16, 'value' : '=G#+S#',      'format' : {'bg_color':'c7dcff', 'num_format': '$#,##0.00'}},
                { 'title' : _('мин. партия'),                    'width' : 16, 'attr' : 'get_md_start', 'format' : {'bg_color':'c7dcff'}},]
        else:
            whoosale = [
                { 'title' : _('Мелкий опт'),                     'width' : 16, 'attr' : 'get_sm_price', 'format' : {'bg_color':'deeaff', 'num_format': '$#,##0.00'}},
                { 'title' : _('Цена с достаыкой'),               'width' : 16, 'value' : '=G#+S#',      'format' : {'bg_color':'deeaff', 'num_format': '$#,##0.00'}},
                { 'title' : _('мин. партия'),                    'width' : 16, 'attr' : 'pieces_in_box', 'format' : {'bg_color':'deeaff'}},]
        
        delivery = [{ 'title' : _('Цена доставки 1 шт'),      'width' : 24, 'value' : '=Q#/R#*10', 'format' : {'num_format': '$#,##0.00'}}]

    pos = 6
    for i in range(len(whoosale)):
        data.insert(pos + i, whoosale[i])
    data = data + delivery
        
    # Titles
    # row = []
    for i, field in enumerate(data):
        cell_format = workbook.add_format({ 
            'bold': True, 'align': 'left', 'valign':'top', 'text_wrap':True, 'bg_color':'a8ffb8'
        })
        ws.write(0, i, field['title'], cell_format)
        ws.set_column(i, i, field['width'])

    n = 0
    nn = 0
    products_pks = [product.pk for product in products]



    for categoty in Category.objects.distinct().filter(products__in=products):
        n += 1
        ws.set_row(n, 32)
        cell_format = workbook.add_format({ 
            'bold': True, 'align': 'center', 'valign':'middle', 'font_size' : 24,'text_wrap':True, 'bg_color':'e3bdfc'
        })
        ws.merge_range(f'A{n+1}:Y{n+1}', categoty.name, cell_format)
        for i, product in enumerate(categoty.products.filter(pk__in=products_pks)):
            n += 1
            nn += 1
            ws.set_row(n, 124)
            for j, field in enumerate(data):
                format_options = {'align': 'left', 'valign':'top', 'text_wrap':True, }
                if 'format' in field.keys():
                    format_options.update(field['format'])
                cell_format = workbook.add_format(format_options)

                value = '-'
                write = True
                # Number
                if 'attr' in field.keys():
                    attr = field['attr']
                    # Number
                    if attr == 'num': 
                        value = nn
                    # Image
                    elif attr == 'image':
                        options = {'x_offset': 3,'y_offset': 3,'x_scale': 1,'y_scale': 1,'object_position': 1}
                        imgs = product.images.all()
                        if len(imgs) > 0:
                            ws.insert_image(n, j, settings.MEDIA_ROOT + imgs[0].image_xs.name, options)
                            write = False
                    # Price
                    elif attr in ['get_sm_price','get_md_price','get_bg_price']:
                        x = float(getattr(product, field['attr']))
                        value = eval(priceFormula)
                        
                    elif attr == 'price':
                        whoosale = {
                            'small':'sm', 'middle':'md', 'big':'bg'
                        }
                        if 'whoosale' in request.GET:
                            value = getattr(product, f"get_{whoosale[request.GET.get('whoosale')]}_price")
                        else:
                            value = product.price
                        if product.category.ignore_multiply == False:
                            x = float(value)
                            value = eval(priceFormula)
                        
                    # Links
                    elif attr == 'link':
                        value = '/'
                    # Other
                    else: value = getattr(product, field['attr'])
                elif 'value' in field.keys():
                    value = field['value'].replace('#',str(n+1))
                
                if write == True:
                    ws.write(n, j, value, cell_format)
    # Close the workbook before sending the data.
    workbook.close()
    # Rewind the buffer.
    output.seek(0)

    # Set up the Http response.
    filename = f"products_{slugify(priceFormula.replace('.','-'))}.xlsx"
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def products_zip(request, ids=None):
    if ids != None:
        ids = ids.split('-')
        products = Product.objects.filter(pk__in=ids) 
    else:
        products = Product.objects.all() 
    

    folderName = {
        'images' : _('Фото'),
        'documents' : _('Документы'),
        'certificates' : _('Сертификаты'),
    }

    lenProducts = len(products)
    
    mem_file = BytesIO()
    with zipfile.ZipFile(mem_file, "w") as zip_file:
        length = len(products)
        for num, product in enumerate(products):
            print(f'Запаковано {num+1} из {length}')
            productFolder = [' '.join([product.code,'-',product.trans.name])]
            if lenProducts > 1:
                productFolder.insert(0, product.category.trans.name)
            
            for i, folder in enumerate(['images','documents', 'certificates']):
                files = getattr(product,folder).all()
                attr = 'file'
                if folder == 'images':
                    attr = 'image_l'
                for n, f in enumerate(files):

                    fName = str(n)
                    if hasattr(f, 'name'):
                        fName = f.name

                    file_path = settings.MEDIA_ROOT + getattr(f, attr).name
                    if os.path.exists(file_path):
                        zip_file.write(
                            settings.MEDIA_ROOT + getattr(f, attr).name, 
                            "\\".join(productFolder + [folderName[folder], str(n+1) + '. ' + fName + '.' + f.ext]), 
                            zipfile.ZIP_DEFLATED
                        )
    mem_file.seek(0) 
    response = HttpResponse(mem_file, content_type='application/zip')
    if lenProducts == 1:
        filename = slugify(unidecode('_'.join([product.code, product.name])))
    else:
        date = datetime.now().strftime('%d-%m-%y')
        filename = 'products_' + date
    response['Content-Disposition'] = f'attachment; filename={filename}.zip'
    return response


