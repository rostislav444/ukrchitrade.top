from django.db import models
from apps.core.models import NameSlug


class Attribute(NameSlug):
    name =  models.CharField(max_length=100, blank=False, verbose_name="Название", unique=True)
    slug =  models.CharField(max_length=250, blank=True, null=True, verbose_name="Иденитификатор", editable=False)

    class Meta:
        verbose_name = "Группа атрибутов"
        verbose_name_plural = "Группы атрибутов"

    def __str__(self):
        return self.name


class AttributeValue(NameSlug):
    parent = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='values')
    name =   models.CharField(max_length=100, blank=False, verbose_name="Название")
    slug =   models.CharField(max_length=250, blank=True, null=True, verbose_name="Иденитификатор", editable=False)

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"
        unique_together = ['parent', 'name']


class CategoryAttribute(models.Model):
    parent =         models.ForeignKey('catalogue.Category',  on_delete=models.CASCADE, related_name='attributes', verbose_name='Катгория')
    attribute =      models.ForeignKey(Attribute,             on_delete=models.CASCADE, related_name='category',   verbose_name='Группа атрибутов')
    attribute_pk =   models.PositiveIntegerField(default=0, editable=False)
    values =         models.ManyToManyField(AttributeValue,   through="CategoryAttributeValue")
    
        
    class Meta:
        unique_together = ['parent', 'attribute']
        verbose_name = "Связь атрибутов с категрией"
        verbose_name_plural = "Связи атрибутов с категриями"

    def __str__(self):
        return f'{self.parent.name} > {self.attribute.name}'

    def save(self):
        super(CategoryAttribute, self).save()
        if self.attribute_pk != self.attribute.pk:
            self.category_values.all().delete()
            for value in self.attribute.values.all():
                self.values.add(value)
            self.attribute_pk = self.attribute.pk
            super(CategoryAttribute, self).save()

    @property
    def get_attributes_values(self):
        values = CategoryAttributeValue
        values = self.category_values.all().values_list('value', flat=True)
        return AttributeValue.objects.filter(pk__in=values)

    @property
    def get_values(self):
        return self.values.all()
        

class CategoryAttributeValue(models.Model):
    parent =    models.ForeignKey(CategoryAttribute,  on_delete=models.CASCADE, related_name='category_values', verbose_name='Связь атрибутов с категрией')
    value =     models.ForeignKey(AttributeValue,     on_delete=models.CASCADE, related_name='category_values', verbose_name='Атрибут')

    class Meta:
        unique_together = ['parent', 'value']

    def __str__(self):
        return f'{self.parent.parent.name} > {self.value.name}'

    @property
    def get_value(self):
        return value.value.name

    class Meta:
        verbose_name = "Атрибут категрии"
        verbose_name_plural = "Атрибуты категрий"
        unique_together = ['parent', 'value']


class ProductAttribute(models.Model):
    parent =    models.ForeignKey('catalogue.Product',    on_delete=models.CASCADE, related_name='product_attrs')
    attribute = models.ForeignKey(CategoryAttribute,      on_delete=models.CASCADE, related_name='product_attrs')
    value =     models.ManyToManyField(AttributeValue, blank=True, related_name='product_attrs')

    # def __str__(self):
    #     return f'Атрибут: {self.attribute.attribute.name} - {self.value}'.upper()