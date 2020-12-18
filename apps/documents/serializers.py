from rest_framework import serializers
from apps.documents.models import Invoice, InvoiceProducts, InvoiceTemplate, PriceFormula, Incoterms

from django.utils.translation import gettext as _
import json


class PriceFormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceFormula
        fields = ['pk', 'formula']



class IncotermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incoterms
        fields = ['pk', 'name','formula']


class InvoiceLiteSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d.%m.%Y")

    class Meta:
        model = Invoice
        fields = ['pk', 'code', 'date']


class InvoiceTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceTemplate
        fields = ['pk', 'name']


class InvoiceProductSerializer(serializers.ModelSerializer):
    id =   serializers.CharField(read_only=True, source="product.pk")
    name = serializers.CharField(read_only=True, source="product.name")
    code = serializers.CharField(read_only=True, source="product.code")
    pieces_in_box = serializers.CharField(read_only=True, source="product.pieces_in_box")
    

    class Meta:
        model = InvoiceProducts
        fields = ['id','code', 'name', 'image', 'quantity', 'pieces_in_box']



class InvoiceSerializer(serializers.ModelSerializer):
    invoices =    serializers.SerializerMethodField(label=_('Инвойсы'))
    template =    serializers.IntegerField(label=_('Шаблон'),read_only=True, source="template.pk")
    templates =   serializers.SerializerMethodField(label=_('Шаблоны'))
    price =       serializers.IntegerField(label=_('Формула цен'), read_only=True, source="price.pk")
    prices =      serializers.SerializerMethodField(label=_('Формулы цен'))
    incoterms =   serializers.IntegerField(label=_('Инкотермс'),read_only=True, source="incoterms.pk")
    incotermses = serializers.SerializerMethodField(label=_('Компании'))
    products =  InvoiceProductSerializer(many=True, read_only=True)
    date =      serializers.DateField(format="%d.%m.%Y")

    class Meta:
        model = Invoice
        fields = [
            'pk','invoices','code','date',
            'template','templates',
            'exporter','importer',
            'incoterms','incotermses',
            'price','prices',
            'products'
        ]

    def get_invoices(self, object):
        return json.loads(json.dumps(InvoiceLiteSerializer(Invoice.objects.all(), many=True).data))
    
    def get_templates(self, object):
        return json.loads(json.dumps(InvoiceTemplatesSerializer(InvoiceTemplate.objects.all(), many=True).data))

    def get_prices(self, object):
        return json.loads(json.dumps(PriceFormulaSerializer(PriceFormula.objects.all(), many=True).data))

    def get_incotermses(self, object):
        return json.loads(json.dumps(IncotermsSerializer(Incoterms.objects.all(), many=True).data))