from django.db import models

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey('user.user', blank=True, null=True, verbose_name="Пользователь")