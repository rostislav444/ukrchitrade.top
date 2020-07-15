from django import forms
from apps.core.models import PageContacts
from django.utils.translation import gettext as _

class ContactsForm(forms.ModelForm):
    class Meta:
        model = PageContacts
        fields = ['email','name','text']

    def __init__(self, *args, **kwargs):
        super(ContactsForm, self).__init__(*args, **kwargs)
        # E-mail
        self.fields['email'].label = ''
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['data-alert'] =   _('Введите Ваш Email')
        self.fields['email'].widget.attrs['data-error'] =   _('Email имеет не верный формат')
        self.fields['email'].widget.attrs['placeholder'] =  _('Email *')
        # Name
        self.fields['name'].label = ''
        self.fields['name'].required = True
        self.fields['name'].widget.attrs['data-alert'] =   _('Введите Ваше имя')
        self.fields['name'].widget.attrs['placeholder'] =  _('Ваше имя *')
        # Text
        self.fields['text'].label = ''
        self.fields['text'].required = True
        self.fields['text'].widget.attrs['data-alert'] =   _('Вы ничего не написали')
        self.fields['text'].widget.attrs['placeholder'] =  _('Текст письма *')
       
