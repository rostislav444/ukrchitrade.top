from django.apps import AppConfig
from django.apps.registry import Apps
from django.db import models
from django.contrib import admin
from django.apps import apps
from django.forms import TextInput, Textarea
from apps.core.models import Language, Translation
import jsonfield


def create_model(name,parent_model_name=None,fields=None,inherit=models.Model,app_label=None,module='',options=None,admin_parent=None,admin_opts=None):
    class Meta:
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)
    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (inherit,), attrs)

    # Create an Admin class if admin options were provided
    FORMFIELD_OVERRIDES = {
        models.CharField: {'widget': TextInput(attrs={'size':'63'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':61})},
        jsonfield.JSONField: {'widget': Textarea(attrs={'rows':2, 'cols':61})},
    }
    if admin_opts is not None:
        attrs = {
            'formfield_overrides' : FORMFIELD_OVERRIDES,
            'model': model,
            'extra': 0,
            '__module__': 'apps.' + app_label + '.admin',
            'sortable_options' : 'parent'
        }
        admin_model = type(parent_model_name + "TranslationInline", (admin.StackedInline,), attrs)

        if admin_parent != None:
            if len(admin_parent.inlines) == 0:
                admin_parent.inlines = []
            admin_parent.inlines.append(admin_model)

        for key, value in admin_opts:
            setattr(admin_model, key, value)
    return model







def setModelParams(parent_model_name, app_name):
    def getModule(app_name=None):
        module = __import__('apps')
        path = app_name + '.admin'
        for directory in path.split('.'):
            module = getattr(module, directory)
        return module
        
        
    module = getModule(app_name)
    admin_parent = getattr(module, parent_model_name + 'Admin')
    model_name = parent_model_name + 'Translation'
    # FIELDS
    fields = {
        'parent' : models.ForeignKey(app_name + '.' + model.__name__, on_delete=models.CASCADE, related_name='translation')
    }

    for field in model._meta.get_fields(include_hidden=False):
        if field.get_internal_type() in ['CharField', 'TextField'] and 'json' not in str(field.name).lower():
            fields[field.name] = field
    # OPTIONS
    options = {}
    for option in ['verbose_name', 'verbose_name_plural']:
        if hasattr(model._meta, option):
            options[option] = getattr(model._meta, option) + ' (перевод)'
    # CREATE MODEL
    model = create_model(
        app_label=app_name, 
        name=model_name, 
        parent_model_name = parent_model_name,
        inherit=Language, 
        fields=fields, 
        options=options, 
        module=model.__module__, 
        admin_opts={},
        admin_parent=admin_parent
    )








