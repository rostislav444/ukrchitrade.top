from django.db import models
from django.utils.timezone import now
from apps.core.models import Translation, NameSlug
from apps.core.models import *
import requests, datetime

class Currency(NameSlug):
    code = models.CharField(max_length=100, blank=False, editable=True, verbose_name='Код')
    base = models.BooleanField(default=False, verbose_name='Базовая валюта')

    class Meta:
        ordering = ['-base']
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
    
    def __str__(self):
        return self.code

    def get_exchange_rate(self):
        if self.base:
            response = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json').json()
            currencies = Currency.objects.exclude(pk=self.pk)
            currencies_codes = currencies.values_list('code', flat=True)
            for c in response:
                code, value = c['cc'], c['rate']
                if code in currencies_codes:
                    currency = currencies.get(code=code)
                    print( currency)
                    try:
                        exchange = CurrencyExchage.objects.get(parent=self, currency=currency)
                    except:
                        exchange = CurrencyExchage(parent=self, currency=currency)
                    exchange.value = value
                    exchange.save()

    def save(self):
        self.get_exchange_rate()
        self.code = self.code.upper()
        if self.base:
            try:
                temp = Currency.objects.get(base=True)
                if self != temp:
                    temp.base = False
                    temp.save()
            except Currency.DoesNotExist:
                pass
        super(Currency, self).save()
   

class CurrencyExchage(models.Model):
    parent =   models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='Валюта')
    value =    models.DecimalField(default=0, decimal_places=4, max_digits=200, verbose_name='Обменный курс')
    date =     models.DateField(default=now)

    class Meta:
        ordering = ('currency',)
        unique_together = ('parent', 'currency',)
        verbose_name = 'Обменный курс'
        verbose_name_plural = 'Обменные курсы'

    def save(self):
        self.update = datetime.datetime.now()
        super(CurrencyExchage, self).save()
