from rest_framework import serializers

from funds.models import Accounts, Categories, Postings, Transactions, Budgets


class AccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Accounts
        fields = ['url', 'id', 'account_name', 'created_date', 'account_type']


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Categories
        fields = ['url', 'id', 'category_name', 'created_date']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    account_id = AccountSerializer(many=False, read_only=True)
    categories_id = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Transactions
        fields = [
            'url', 'id', 'posting_num', 'account_id',
            'categories_id', 'amount', 'note'
        ]


class PostingSerializer(serializers.HyperlinkedModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Postings
        fields = [
            'url', 'posting_num', 'date', 'posting_type',
            'payee', 'cleared', 'note', 'transactions'
        ]


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    categories_id = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Budgets
        fields = ['url', 'id', 'month', 'year', 'categories_id', 'amount']
