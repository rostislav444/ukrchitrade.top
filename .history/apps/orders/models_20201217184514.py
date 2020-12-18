from django.db import models

# Create your models here.
class Order(models.Model):
    user =        models.ForeignKey('user.user', blank=True, null=True, verbose_name="Пользователь")
    phone =       models.CharField(max_length=40, blank=True, null=True)
    name =        models.CharField(max_length=50, blank=True, editable=True, verbose_name='Имя')
    surname =     models.CharField(max_length=50, blank=True, editable=True, verbose_name='Фамилия')
    patronymic =  models.CharField(max_length=50, blank=True, editable=True, verbose_name='Отчество')


class OrderProduct(models.Model):
    parent =    models.ForeignKey(Order, verbose_name="Продукт")
    product =   models.ForeignKey('catalogue.Product', verbose_name="Продукт")
    quantity =  models.PositiveIntegerField(default=1, verbose_name='Количество')
    price =     models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Розничная')
    price_ua =  models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Розничная, грн.')
    total =     models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Всего')
    total_ua =  models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Всего, грн.')
    