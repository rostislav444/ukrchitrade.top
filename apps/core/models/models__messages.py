from django.db import models
from ckeditor.fields import RichTextField


class Message(models.Model):
    subject =    models.CharField(blank=False,  max_length=255, verbose_name='Тема письма')
    date =       models.DateTimeField(auto_now=True, verbose_name='Время отправки')
    first_name = models.CharField(blank=False, max_length=255, verbose_name='Имя')
    email =      models.CharField(blank=False, max_length=255, verbose_name='Email')
    phone =      models.CharField(blank=True,  max_length=255, verbose_name='Телефон')
    text =       RichTextField(blank=False,    verbose_name='Текст письма')
    
    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'