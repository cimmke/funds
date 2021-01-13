from rest_framework import viewsets

from funds.models import Accounts, Categories, Postings, Transactions, Budgets
from funds.serializers import (
    AccountSerializer,
    CategorySerializer,
    PostingSerializer,
    TransactionSerializer,
    BudgetSerializer
)


class AccountsViewset(viewsets.ModelViewSet):
    """
    Viewset for the Accounts table
    """
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer


class CategoriesViewset(viewsets.ModelViewSet):
    """
    Viewset for the Categories table
    """
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class PostingsViewset(viewsets.ModelViewSet):
    """
    Viewset for the Postings table
    """
    queryset = Postings.objects.all()
    serializer_class = PostingSerializer


class TransactionsViewset(viewsets.ModelViewSet):
    """
    Viewset for the Transactions table
    """
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer


class BudgetsViewset(viewsets.ModelViewSet):
    """
    Viewset for the Budgets table
    """
    queryset = Budgets.objects.all()
    serializer_class = BudgetSerializer
