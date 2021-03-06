# Generated by Django 3.1.5 on 2021-01-11 16:55

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import funds.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=50, unique=True)),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccountTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Postings',
            fields=[
                ('posting_num', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=datetime.date.today)),
                ('payee', models.CharField(blank=True, max_length=50)),
                ('cleared', models.BooleanField(default=False)),
                ('note', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostingTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posting_types', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=19)),
                ('note', models.TextField(blank=True)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='funds.accounts')),
                ('categories_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='funds.categories')),
                ('posting_num', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='funds.postings')),
            ],
        ),
        migrations.AddField(
            model_name='postings',
            name='posting_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='funds.postingtypes'),
        ),
        migrations.CreateModel(
            name='Budgets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.SmallIntegerField(default=funds.models.get_month, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('year', models.SmallIntegerField(default=funds.models.get_year)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=19)),
                ('categories_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='funds.categories')),
            ],
        ),
        migrations.AddField(
            model_name='accounts',
            name='account_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='funds.accounttypes'),
        ),
    ]
