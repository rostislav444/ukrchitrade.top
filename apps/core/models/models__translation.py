from django.db import models
from googletrans import Translator
from textblob import TextBlob
from project import settings
from django.utils.translation import get_language as lang
from django.http import QueryDict
from django.apps import apps


class Languages(models.Model):
    code =  models.CharField(max_length=10,  unique=True, choices=settings.LANGUAGES)
    name =  models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)
   

    class Meta:
        verbose_name = 'Активный язык'
        verbose_name_plural = 'Активные языки'

    def __str__(self):
        return self.code + ' - ' + self.name

    def save(self):
        self.name = dict(settings.LANGUAGES)[self.code]
        super(self.__class__, self).save()


def TranslatorsTranslate(text, language):
    if language == 'ru': 
        translation = text
    else:
        try:
            blob = TextBlob(text)
            translation = blob.translate(to=language)
        except: 
            try:
                translator = Translator()
                translation = translator.translate(text, dest=language).text
            except: translation = text
    return str(translation)


class Language(models.Model):
    translate = models.BooleanField(default=True, verbose_name="Перевести")
    language =  models.ForeignKey('core.Languages', blank=False, on_delete=models.CASCADE, verbose_name="Язык")
    
    class Meta:
        abstract = True

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __str__(self):
        return str(self.language.code)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

       
    def save(self):
        translate_childs = False
        if hasattr(self.parent, 'translate_childs'):
            translate_childs = getattr(self.parent, 'translate_childs')
        if self.translate == True or self.parent.translate_childs == True:
            print(self)
            translator = Translator()
            for field in self.parent._meta.get_fields():
                if field.get_internal_type() in ['CharField','TextField']:
                    text = getattr(self.parent, field.name)

                    if text != None:
                        if len(text) > 0:
                            try:    translation = int(text)
                            except: translation = TranslatorsTranslate(text, self.language.code)
                            setattr(self, field.name, translation)
        try:
            self.slug = slugify(str(unidecode.unidecode(self.parent.slug + '-' + str(self.language.code))))
        except: pass
        self.translate = False
        super(Language, self).save()





# ABSTRACT
class Translation(models.Model):
    translate_childs = models.BooleanField(default=False, verbose_name='Перевод')

    class Meta:
        abstract = True

    def __str__(self):
        return 'qwe'
        
    @property
    def translate(self):
        try: return self.translation.get(language__code=lang())
        except: return self

    @property
    def trans(self):
        try: return self.translation.get(language__code=lang())
        except: return self

    @property
    def lang(self):
        tr = {}
        for language in Languages.objects.all():
            code = language.code
            if code == 'zh-hans' or code == 'zh-cn':
                code = 'cn'
            try: tr[code] = self.translation.get(language__code=language.code)
            except: tr[code] = self
        query_dict = QueryDict('', mutable=True)
        query_dict.update(tr)
        return query_dict


   

    def save(self):
        super(Translation, self).save()
        if self.translate_childs:
            ModelTranslation = apps.get_model(self._meta.app_label, self._meta.model_name +'Translation')
            # TRANSLATE
            for language in Languages.objects.all():
                try:    child = ModelTranslation.objects.get(parent=self, language=language)
                except: child = ModelTranslation(parent=self, language=language)
                child.translate = True
                child.save()
            self.translate_childs = False
            super(Translation, self).save()