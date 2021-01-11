import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


def get_month():
    """
    Get the integer value to use for the default month value for a budget
    """
    today = datetime.date.today()
    # If past the first week of the month, return the int value of the next month
    if today.day > 7:
        if today.month == 12:
            return 1
        else:
            return today.month + 1
    else:
        return today.month


def get_year():
    """
    Get the integer value of the year for the default year value for a budget
    """
    today = datetime.date.today()
    if today.day > 7 and today.month == 12:
        return today.year + 1
    else:
        return today.year


class AccountTypes(models.Model):
    account_type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.account_type


class Accounts(models.Model):
    account_name = models.CharField(max_length=50, unique=True)
    created_date = models.DateField(auto_now_add=True)
    account_type = models.ForeignKey(AccountTypes, on_delete=models.PROTECT)

    def __str__(self):
        return self.account_name


class PostingTypes(models.Model):
    posting_types = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.posting_types


class Categories(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Postings(models.Model):
    posting_num = models.PositiveIntegerField(primary_key=True)
    date = models.DateField(default=datetime.date.today)
    posting_type = models.ForeignKey(PostingTypes, on_delete=models.PROTECT)
    payee = models.CharField(max_length=50, blank=True)
    cleared = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    def __str__(self):
        return f'{self.posting_num}: {self.date}: {self.payee}'


class Transactions(models.Model):
    posting_num = models.ForeignKey(Postings, on_delete=models.PROTECT)
    account_id = models.ForeignKey(Accounts, on_delete=models.PROTECT)
    categories_id = models.ForeignKey(Categories, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    note = models.TextField(blank=True)

    def __str__(self):
        return f'{self.posting_num}: {self.account_id}: {self.amount}'


class Budgets(models.Model):
    month = models.SmallIntegerField(
        default=get_month,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    year = models.SmallIntegerField(default=get_year)
    categories_id = models.ForeignKey(Categories, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=19, decimal_places=4)

    def __str__(self):
        return f'{self.month}/{self.year}: {self.categories_id}'
