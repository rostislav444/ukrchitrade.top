# DAJNGO
from django.db import models
from django.db.models.signals import pre_init
from django.utils.translation import get_language
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# APPS
from apps.core.models import Translation
from project import settings
# OTHER
# from googletrans import Translator
import urllib.request
import urllib.parse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_manager = True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractBaseUser):
    # CONTACTS
    email =           models.EmailField(blank=False, unique=True, max_length=500)
    email_confirmed = models.BooleanField(default=False)
    phone =           models.CharField(max_length=40, blank=True, null=True)
    phone_confirmed = models.BooleanField(default=False)
    # PERSONAL INFO
    name =            models.CharField(max_length=50, blank=True, editable=True, verbose_name='Имя')
    surname =         models.CharField(max_length=50, blank=True, editable=True, verbose_name='Фамилия')
    patronymic =      models.CharField(max_length=50, blank=True, editable=True, verbose_name='Отчество')
    # PASSWORD
    password =        models.CharField(max_length=500, blank=True)
    # PERMISION
    is_admin =        models.BooleanField(default=False)  
    is_active =       models.BooleanField(default=False)
    was_active =      models.BooleanField(default=False)
    is_manager =      models.BooleanField(default=False)
    is_client =       models.BooleanField(default=False)
        
    # DATETIME
    created =         models.DateTimeField(default=now)

    objects = CustomUserManager()
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-created']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    
    def save(self, *args, **kwargs):
        super(CustomUser, self).save()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_staff(self):
        return self.is_admin



class Wishlist(models.Model):
    user =    models.ForeignKey(CustomUser,          on_delete=models.CASCADE, verbose_name='Пользователь', related_name='products')
    product = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE, verbose_name='Товар')
    date =    models.DateTimeField(default=now)

    class Meta:
        ordering = ['-date']
        unique_together = [['user', 'product']]

    def __str__(self):
        return ''








