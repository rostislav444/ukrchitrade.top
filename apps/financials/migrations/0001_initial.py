# Generated by Django 2.2.10 on 2020-05-11 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate_childs', models.BooleanField(default=False, verbose_name='Перевод')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.CharField(blank=True, editable=False, max_length=250, null=True, verbose_name='Иденитификатор')),
                ('adress', models.CharField(max_length=100, verbose_name='Адрес')),
                ('swift', models.CharField(max_length=250, verbose_name='SWIFT код')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankCorrespondent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate_childs', models.BooleanField(default=False, verbose_name='Перевод')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.CharField(blank=True, editable=False, max_length=250, null=True, verbose_name='Иденитификатор')),
                ('swift', models.CharField(max_length=250, verbose_name='SWIFT код')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate_childs', models.BooleanField(default=False, verbose_name='Перевод')),
                ('organization', models.CharField(blank=True, max_length=250, verbose_name='Организация')),
                ('country', models.CharField(blank=True, max_length=250, verbose_name='Страна')),
                ('city', models.CharField(blank=True, max_length=250, verbose_name='Город')),
                ('adress', models.CharField(blank=True, max_length=250, verbose_name='Адрес')),
                ('name', models.CharField(blank=True, max_length=250, verbose_name='Имя представителя')),
                ('surname', models.CharField(blank=True, max_length=250, verbose_name='Фамилия представителя')),
                ('patronymic', models.CharField(blank=True, max_length=250, verbose_name='Отчество представителя')),
                ('position', models.CharField(blank=True, max_length=100, verbose_name='Должность')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='Телефон')),
                ('fax', models.CharField(blank=True, max_length=40, null=True, verbose_name='Факс')),
                ('email', models.EmailField(blank=True, max_length=500, verbose_name='Email')),
                ('seal', models.ImageField(blank=True, upload_to='company/seal', verbose_name='Печать')),
                ('sign', models.ImageField(blank=True, upload_to='company/sign', verbose_name='Подпись')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate_childs', models.BooleanField(default=False, verbose_name='Перевод')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.CharField(blank=True, editable=False, max_length=250, null=True, verbose_name='Иденитификатор')),
                ('code', models.CharField(max_length=100, verbose_name='Код')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CurrencyTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate', models.BooleanField(default=True, verbose_name='Перевести')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.CharField(blank=True, editable=False, max_length=250, null=True, verbose_name='Иденитификатор')),
                ('code', models.CharField(max_length=100, verbose_name='Код')),
                ('translation', models.BooleanField(default=False, verbose_name='Перевести')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Languages', verbose_name='Язык')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='financials.Currency')),
            ],
            options={
                'verbose_name': 'currency (перевод)',
                'verbose_name_plural': 'currencys (перевод)',
            },
        ),
        migrations.CreateModel(
            name='CompanyTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate', models.BooleanField(default=True, verbose_name='Перевести')),
                ('organization', models.CharField(blank=True, max_length=250, verbose_name='Организация')),
                ('country', models.CharField(blank=True, max_length=250, verbose_name='Страна')),
                ('city', models.CharField(blank=True, max_length=250, verbose_name='Город')),
                ('adress', models.CharField(blank=True, max_length=250, verbose_name='Адрес')),
                ('name', models.CharField(blank=True, max_length=250, verbose_name='Имя представителя')),
                ('surname', models.CharField(blank=True, max_length=250, verbose_name='Фамилия представителя')),
                ('patronymic', models.CharField(blank=True, max_length=250, verbose_name='Отчество представителя')),
                ('position', models.CharField(blank=True, max_length=100, verbose_name='Должность')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='Телефон')),
                ('fax', models.CharField(blank=True, max_length=40, null=True, verbose_name='Факс')),
                ('email', models.EmailField(blank=True, max_length=500, verbose_name='Email')),
                ('translation', models.BooleanField(default=False, verbose_name='Перевести')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Languages', verbose_name='Язык')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='financials.Company')),
            ],
            options={
                'verbose_name': 'company (перевод)',
                'verbose_name_plural': 'companys (перевод)',
            },
        ),
        migrations.CreateModel(
            name='BankTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate', models.BooleanField(default=True, verbose_name='Перевести')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.CharField(blank=True, editable=False, max_length=250, null=True, verbose_name='Иденитификатор')),
                ('adress', models.CharField(max_length=100, verbose_name='Адрес')),
                ('swift', models.CharField(max_length=250, verbose_name='SWIFT код')),
                ('translation', models.BooleanField(default=False, verbose_name='Перевести')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Languages', verbose_name='Язык')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='financials.Bank')),
            ],
            options={
                'verbose_name': 'bank (перевод)',
                'verbose_name_plural': 'banks (перевод)',
            },
        ),
        migrations.CreateModel(
            name='BankCorrespondentTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate', models.BooleanField(default=True, verbose_name='Перевести')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.CharField(blank=True, editable=False, max_length=250, null=True, verbose_name='Иденитификатор')),
                ('swift', models.CharField(max_length=250, verbose_name='SWIFT код')),
                ('translation', models.BooleanField(default=False, verbose_name='Перевести')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Languages', verbose_name='Язык')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='financials.BankCorrespondent')),
            ],
            options={
                'verbose_name': 'bank correspondent (перевод)',
                'verbose_name_plural': 'bank correspondents (перевод)',
            },
        ),
        migrations.CreateModel(
            name='CurrencyExchage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Валюта', to='financials.Currency')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchange', to='financials.Currency')),
            ],
            options={
                'unique_together': {('parent', 'currency')},
            },
        ),
        migrations.CreateModel(
            name='CompanyBankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(blank=True, max_length=250, verbose_name='Номер счета')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.Bank', verbose_name='Банк')),
                ('bank_crspnd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.BankCorrespondent', verbose_name='Банк корреспондент')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.Currency', verbose_name='Валюта счета')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account', to='financials.Company', verbose_name='Компания')),
            ],
            options={
                'unique_together': {('currency', 'bank', 'account')},
            },
        ),
    ]
