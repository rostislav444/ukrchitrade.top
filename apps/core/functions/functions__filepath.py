import unidecode
from django.utils.text import slugify


class UploadTo:
  def __init__(self, name='file'):
    self.name = name

  def __call__(self, instance, filename):
   
    ext = filename.split('.')[-1]
    appName = instance.__module__.split('.')[1]
    modelName = str(instance.__class__.__name__)
    fileName = slugify(unidecode.unidecode(self.name + '_' + str(instance.pk)))
    fileName = fileName + '.' + ext
    path = '/'.join([appName, modelName, fileName])
    return path

  def deconstruct(self):
    app = self.__module__.split('.')
    return ('apps.core.functions.UploadTo', [self.name], {})

