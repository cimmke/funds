from rest_framework import serializers

from funds.models import Accounts


class AccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Accounts
        fields = ['url', 'id', 'account_name', 'created_date', 'account_type']
