# Generated by Django 2.2.10 on 2020-12-14 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20201209_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcharacteristics',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]