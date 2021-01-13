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


class Accounts(models.Model):
    CHECKING = 'checking'
    SAVINGS = 'savings'
    CASH = 'cash'
    CREDIT_CARD = 'credit_card'
    LINE_OF_CREDIT = 'line_of_credit'
    INVESTMENT = 'investment'
    OTHER_LIABILITY = 'other_liability'
    OTHER_ASSET = 'other_asset'
    ACCT_TYPES = [
        (CHECKING, 'Checking'),
        (SAVINGS, 'Savings'),
        (CASH, 'Cash'),
        (CREDIT_CARD, 'Credit Card'),
        (LINE_OF_CREDIT, 'Line of Credit'),
        (INVESTMENT, 'Investment'),
        (OTHER_LIABILITY, 'Other Liability or Loan'),
        (OTHER_ASSET, 'Other Asset'),
    ]
    account_name = models.CharField(max_length=50, unique=True)
    created_date = models.DateField(auto_now_add=True)
    account_type = models.CharField(max_length=30, choices=ACCT_TYPES, default=CASH)

    def __str__(self):
        return self.account_name


class Categories(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Postings(models.Model):
    STANDARD = 'standard'
    INCOME = 'income'
    TRANSFER = 'transfer'
    POST_TYPES = [
        (STANDARD, 'Standard'),
        (INCOME, 'Income'),
        (TRANSFER, 'Transfer'),
    ]
    posting_num = models.PositiveIntegerField(primary_key=True)
    date = models.DateField(default=datetime.date.today)
    posting_type = models.CharField(
        max_length=30,
        choices=POST_TYPES,
        default=STANDARD
    )
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
