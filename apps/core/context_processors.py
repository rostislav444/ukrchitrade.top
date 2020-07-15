from apps.core.models import SiteText
from django.utils.translation import get_language as lang
from apps.core.models import Languages
from django.contrib.sites.shortcuts import get_current_site
import datetime


def cur_time(request):
    time = datetime.datetime.now()
    return {'time' : time}


def language_change(request):
    languages = {}
    current_lang = lang()
    
    if request.is_secure():
        scheme = 'https'
    else: scheme = 'http'
    base_url = ''.join([scheme,'://',request.META['HTTP_HOST'],'/'])

    path = str(request.path).replace('/' + str(current_lang) + '/', '')
    for language in Languages.objects.all():
        languages[language.code] = { 'path' : base_url+'/'.join([language.code,path]) , 'active' : True if language.code == current_lang else False}
    return {'languages':languages, 'current_lang':current_lang}