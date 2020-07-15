from django.contrib import admin
from .models import *


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    pass


