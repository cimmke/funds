from rest_framework import viewsets

from funds.models import Accounts
from funds.serializers import AccountSerializer


class AccountsViewset(viewsets.ModelViewSet):
    """
    Viewset for the Accounts table
    """
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer
