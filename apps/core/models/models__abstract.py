
from django.db import models
from django.contrib import admin
from django.utils.text import slugify
from django.core.validators import MaxLengthValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from project import settings
from PIL import Image
# TRANSLATORS
from django.utils.translation import get_language as lang

import unidecode
import os
from django.apps import apps
import django
from django.contrib.contenttypes.models import ContentType
from shutil import copyfile
import jsonfield


# SEO
class Seo(models.Model):
    seo_title =       models.CharField(max_length=70,  blank=True, null=True, help_text="До 70 символов",  validators=[MaxLengthValidator(70)])
    seo_description = models.TextField(max_length=300, blank=True, null=True, help_text="До 300 символов", validators=[MaxLengthValidator(300)])
    seo_keywords =    models.TextField(max_length=255, blank=True, null=True, help_text="До 255 символов", validators=[MaxLengthValidator(255)])

    class Meta:
        abstract = True


class NameSlug(models.Model):
    name =  models.CharField(max_length=100, blank=False, verbose_name="Название")
    slug =  models.CharField(max_length=250, blank=True, null=True, verbose_name="Иденитификатор", editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(unidecode.unidecode(self.name))
        super(NameSlug, self).save()


class TitleText(models.Model):
    name =  models.CharField(blank=False, max_length=100, verbose_name="Название")
    text =  models.TextField(blank=False, verbose_name="Текст")
    slug =  models.CharField(blank=True,  max_length=250, null=True, verbose_name="Иденитификатор")

    class Meta:
        abstract = True

    def save(self):
        if self.slug == None:
            try:
                translator = Translator()
                translation = translator.translate(self.name, dest='en').text
            except: 
                translation = unidecode.unidecode(self.name)
            self.slug = slugify(str(translation))
            if hasattr(self, 'parent'):
                if getattr(self, 'parent') != None:
                    self.slug = self.parent.slug + '_' + self.slug
            self.slug = str(self.slug).replace('-','_')
        super(TitleText, self).save()





           


    



