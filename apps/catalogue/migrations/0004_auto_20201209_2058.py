# Generated by Django 2.2.10 on 2020-12-09 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20201209_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcharacteristics',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
