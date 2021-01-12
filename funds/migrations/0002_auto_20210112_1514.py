# Generated by Django 3.1.5 on 2021-01-12 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttypes',
            name='account_type',
            field=models.CharField(choices=[('checking', 'Checking'), ('savings', 'Savings'), ('cash', 'Cash'), ('credit_card', 'Credit Card'), ('line_of_credit', 'Line of Credit'), ('investment', 'Investment'), ('other_liability', 'Other Liability or Loan'), ('other_asset', 'Other Asset')], max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='postingtypes',
            name='posting_types',
            field=models.CharField(choices=[('standard', 'Standard'), ('income', 'Income'), ('transfer', 'Transfer')], max_length=50, unique=True),
        ),
    ]