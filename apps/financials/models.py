from django.db import models
from apps.core.models import Translation, NameSlug
from apps.core.models import *

class Currency(Translation, NameSlug):
    code = models.CharField(max_length=100, blank=False, editable=True, verbose_name='Код')
   

class CurrencyExchage(models.Model):
    parent = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='Валюта')

    class Meta:
        unique_together = ('parent', 'currency',)


class Bank(Translation, NameSlug):
    adress = models.CharField(max_length=100, blank=False, editable=True, verbose_name='Адрес')
    swift = models.CharField(max_length=250, blank=False, editable=True, verbose_name='SWIFT код')


class BankCorrespondent(Translation, NameSlug):
    swift = models.CharField(max_length=250, blank=False, editable=True, verbose_name='SWIFT код')


class Company(Translation):
    organization =    models.CharField(max_length=250, blank=True, editable=True, verbose_name='Организация')
    country =         models.CharField(max_length=250, blank=True, editable=True, verbose_name='Страна')
    city =            models.CharField(max_length=250, blank=True, editable=True, verbose_name='Город')
    adress =          models.CharField(max_length=250, blank=True, editable=True, verbose_name='Адрес')
    name =            models.CharField(max_length=250, blank=True, editable=True, verbose_name='Имя представителя')
    surname =         models.CharField(max_length=250, blank=True, editable=True, verbose_name='Фамилия представителя')
    patronymic =      models.CharField(max_length=250, blank=True, editable=True, verbose_name='Отчество представителя')
    position =        models.CharField(max_length=100, blank=True, editable=True, verbose_name='Должность')
    phone =           models.CharField(blank=True,  max_length=40,  null=True,  verbose_name='Телефон')
    fax  =            models.CharField(blank=True,  max_length=40,  null=True,  verbose_name='Факс')
    email =           models.EmailField(blank=True, max_length=500, unique=True, verbose_name='Email')
    seal =            models.ImageField(blank=True, upload_to='company/seal', verbose_name='Печать')
    sign =            models.ImageField(blank=True, upload_to='company/sign', verbose_name='Подпись')

    @property
    def uah(self):
        try: return self.account.get(currency__code='uah')
        except: return ' -/- '

    @property
    def usd(self):
        try:  return self.account.get(currency__code='usd')
        except: return ' -/- '



class CompanyBankAccount(models.Model):
    parent =      models.ForeignKey('financials.Company',  on_delete=models.CASCADE, verbose_name='Компания', related_name='account')
    currency =    models.ForeignKey('financials.Currency', on_delete=models.CASCADE, verbose_name='Валюта счета')
    bank =        models.ForeignKey('financials.Bank',     on_delete=models.CASCADE, verbose_name='Банк')
    bank_crspnd = models.ForeignKey('financials.BankCorrespondent', on_delete=models.CASCADE, verbose_name='Банк корреспондент')
    account =     models.CharField(max_length=250, blank=True, editable=True, verbose_name='Номер счета')

    class Meta:
        unique_together = ('currency', 'bank', 'account')