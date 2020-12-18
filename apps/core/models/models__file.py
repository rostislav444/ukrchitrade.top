from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from project import settings
import os


def imageFilename(self, filename):
    ext = filename.split('.')[-1]
    app_name = self._meta.app_label
    model_name = self._meta.model_name
    name_attrs = ['id'+str(self.pk)]
    name = ''
    parent = self
    models_attrs = ['slug','code']
    while parent != None:
        for attr in models_attrs:
            if hasattr(parent, attr):
                if getattr(parent, attr) != None:
                    name_attrs.insert(0, str(getattr(parent, attr)))
        if hasattr(parent, 'brand'):
            name_attrs.insert(0, str(parent.brand.slug))
        if hasattr(parent, 'parent'):
            parent = parent.parent
        else:
            parent = None
    name = '_'.join(name_attrs)
    name = slugify(str(name))
    
    # APP NAME PATH
    app_name_path = settings.MEDIA_ROOT + app_name + '/'
    app_name_dir =   os.path.isdir(app_name_path)
    if app_name_dir == False:
        os.mkdir(app_name_path)

    # MODEL NAME PATH
    model_name_path = settings.MEDIA_ROOT + app_name + '/' + model_name + '/'
    model_name_dir = os.path.isdir(model_name_path)
    if model_name_dir == False:
        os.mkdir(model_name_path)
    path =  '/'.join([app_name, model_name])
    return path, name, ext


class OneFile(models.Model):
    num =        models.PositiveIntegerField(default=0, blank=True, verbose_name="Номер") 
    name =       models.CharField(max_length=100, blank=True, default="", verbose_name="Название")
    slug =       models.CharField(max_length=250, blank=True, null=True, verbose_name="Иденитификатор", editable=False)
    file =       models.FileField(upload_to='temp', blank=False, null=True)
    file_url =   models.CharField(max_length=1000, blank=True, editable=False)
    ext =        models.CharField(max_length=100, blank=True, editable=False, verbose_name="file extension")

    class Meta:
        ordering = ['-num']
        abstract = True

    def save(self):
        print(self.file.name)
        super(OneFile, self).save()

        if len(self.name) == 0:
            try:
                modelName =  self.__class__._meta.verbose_name.title()
                self.name = ' '.join([modelName, self.product.category.name, self.product.name, self.product.code])
            except:
                self.name = self.__class__.__name__
      

        self.slug = slugify(unidecode.unidecode(self.name) + '-' + str(self.pk))
        if self.file.url != '/media/' + self.file_url:
            path, name, ext = imageFilename(self, self.file.name)
            self.ext = ext.lower()
            
            # f_name = 

            filename =  f'{path}/{self.slug}.{ext}'
            tempFile = self.file.name
            with open(settings.MEDIA_ROOT + self.file.name, "rb") as f1:
                raw = f1.read()
                with open(settings.MEDIA_ROOT + filename, 'wb') as f:
                    f.write(raw)

            setattr(getattr(self, 'file'), 'name', filename)
            setattr(self, 'file_url', filename)

            try: os.remove(settings.MEDIA_ROOT + tempFile)
            except: pass
            
        super(OneFile, self).save()


    def delete(self):
        try:
            os.remove(settings.MEDIA_ROOT + self.file.name)
        except: pass
        super(OneFile, self).delete()