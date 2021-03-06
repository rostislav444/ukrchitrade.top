from django.shortcuts import render
from django.http import JsonResponse
from apps.core.models.models__pages import *
from apps.core.forms import ContactsForm
from apps.core.functions import SendMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
import datetime
from sentry_sdk import capture_message





args = {}

def robots(request):
    # content = 'any string generated by django'
    # return HttpResponse(content, content_type='text/plain')
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html, content_type='text/plain')






def Contacts(request):
    args = {}
    if request.method == 'POST':
        form = ContactsForm(request.POST)
        if form.is_valid():
            form.save()
            msg =  'Сообщение от ' + request.POST.get('name') + '\n'
            msg += 'E-mail: ' + request.POST.get('email') + '\n'
            msg += 'Текст письма: ' + '\n'
            msg += request.POST.get('text')
            SendMessage(str(msg))
        else:
            args['contacts_form'] = form
    else:
        args['contacts_form'] = ContactsForm()
    return render(request, 'core/pages/contacts.html', args)


def handler404(request, *args, **kwargs):
    capture_message("404", level="error")
    return render(request, '404.html')

def handler500(request, *args, **kwargs):
    capture_message("500", level="error")
    return render(request, '500.html')