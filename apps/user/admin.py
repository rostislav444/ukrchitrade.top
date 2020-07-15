from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.user.models import *

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    inlines = [
      
    ]

    list_display = (
        'email','email_confirmed','phone','phone_confirmed','name','surname','patronymic','created','is_active'
    )
    
    list_filter = (
        'is_admin', 'is_active'
    )
    fieldsets = (
        (None, {'fields': ('name','surname','patronymic','country','city')}),
        ('Организация', {'fields': ('organization','position',)}),
        ('Contacts',    {'fields': ('email','email_confirmed','phone','phone_confirmed','password')}),
        ('Permissions', {'fields': ('is_admin', 'was_active','is_active','is_manager','is_client')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ['-created']
    filter_horizontal = ()
   

