# Generated by Django 2.2.10 on 2020-12-09 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('slug', models.CharField(blank=True, editable=False, max_length=250, null=True, verbose_name='Иденитификатор')),
            ],
            options={
                'verbose_name': 'Группа атрибутов',
                'verbose_name_plural': 'Группы атрибутов',
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.CharField(blank=True, editable=False, max_length=250, null=True, verbose_name='Иденитификатор')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='values', to='catalogue_filters.Attribute')),
            ],
            options={
                'verbose_name': 'Атрибут',
                'verbose_name_plural': 'Атрибуты',
                'unique_together': {('parent', 'name')},
            },
        ),
        migrations.CreateModel(
            name='CategoryAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_pk', models.PositiveIntegerField(default=0, editable=False)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='catalogue_filters.Attribute', verbose_name='Группа атрибутов')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='catalogue.Category', verbose_name='Катгория')),
            ],
            options={
                'verbose_name': 'Связь атрибутов с категрией',
                'verbose_name_plural': 'Связи атрибутов с категриями',
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attrs', to='catalogue_filters.CategoryAttribute')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attrs', to='catalogue.Product')),
                ('value', models.ManyToManyField(blank=True, related_name='product_attrs', to='catalogue_filters.AttributeValue')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_values', to='catalogue_filters.CategoryAttribute', verbose_name='Связь атрибутов с категрией')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_values', to='catalogue_filters.AttributeValue', verbose_name='Атрибут')),
            ],
            options={
                'verbose_name': 'Атрибут категрии',
                'verbose_name_plural': 'Атрибуты категрий',
                'unique_together': {('parent', 'value')},
            },
        ),
        migrations.AddField(
            model_name='categoryattribute',
            name='values',
            field=models.ManyToManyField(through='catalogue_filters.CategoryAttributeValue', to='catalogue_filters.AttributeValue'),
        ),
        migrations.AlterUniqueTogether(
            name='categoryattribute',
            unique_together={('parent', 'attribute')},
        ),
    ]
