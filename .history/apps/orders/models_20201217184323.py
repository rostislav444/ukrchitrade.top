from django.db import models

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey('user.user', blank=True, null=True, verbose_name="Пользователь")


class OrderProduct(models.Model):
    parent =    models.ForeignKey(Order, verbose_name="Продукт")
    product =   models.ForeignKey('catalogue.Product', verbose_name="Продукт")
    price =     models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Розничная')
    price_ua =  models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Розничная, грн.'')
    total =     models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Всего')
    total_ua =  models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name='Всего, грн.')
    