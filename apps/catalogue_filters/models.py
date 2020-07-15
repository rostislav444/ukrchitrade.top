from django.db import models
from apps.core.models import NameSlug


class Attribute(NameSlug):
    def __str__(self):
        return self.name


class AttributeValue(NameSlug):
    parent =    models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='values')


class CategoryAttribute(models.Model):
    parent =    models.ForeignKey('catalogue.Category',  on_delete=models.PROTECT, related_name='attributes')
    attribute = models.ForeignKey(Attribute,             on_delete=models.PROTECT, related_name='category')
    values =    models.ManyToManyField(AttributeValue,   through="CategoryAttributeValue")
        
    class Meta:
        unique_together = ['parent', 'attribute']

    def __str__(self):
        return self.attribute.name

    def save(self):
        super(CategoryAttribute, self).save()

    @property
    def get_attributes_values(self):
        values = self.category_values.all().values_list('value', flat=True)
        return AttributeValue.objects.filter(pk__in=values)


    @property
    def get_values(self):
        return self.values.all()
        

class CategoryAttributeValue(models.Model):
    parent =    models.ForeignKey(CategoryAttribute,  on_delete=models.CASCADE, related_name='category_values')
    value =     models.ForeignKey(AttributeValue,     on_delete=models.CASCADE, related_name='category_values')

    def __str__(self):
        return self.value.name

    @property
    def get_value(self):
        return value.value.name


class ProductAttribute(models.Model):
    parent =    models.ForeignKey('catalogue.Product',    on_delete=models.CASCADE, related_name='product_attrs')
    attribute = models.ForeignKey(CategoryAttribute,      on_delete=models.CASCADE, related_name='product_attrs')
    value =     models.ManyToManyField(AttributeValue, blank=True, related_name='product_attrs')

    # def __str__(self):
    #     return f'Атрибут: {self.attribute.attribute.name} - {self.value}'.upper()