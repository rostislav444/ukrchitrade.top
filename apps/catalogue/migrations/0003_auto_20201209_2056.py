# Generated by Django 2.2.10 on 2020-12-09 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20201209_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCharacteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='catalogue.Product')),
            ],
            options={
                'verbose_name': 'Характеристика',
                'verbose_name_plural': 'Характеристики',
                'ordering': ['-num'],
            },
        ),
        migrations.DeleteModel(
            name='ProductPriceHistory',
        ),
    ]
