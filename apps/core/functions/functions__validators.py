import os
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator





def validateXlsx(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Загрузите таблицу EXCEL в формате .xlsx')


def validateRar(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.rar']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Загрузите архив в формате .rar')
