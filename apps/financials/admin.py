from django.contrib import admin
from .models import *


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    pass

@admin.register(BankCorrespondent)
class BankCorrespondentAdmin(admin.ModelAdmin):
    pass

class CompanyBankAccountInline(admin.TabularInline):
    model = CompanyBankAccount
    extra = 0

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        CompanyBankAccountInline
    ]