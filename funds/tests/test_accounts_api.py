import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from funds.models import Accounts


class AccountsAPITest(APITestCase):

    def setUp(self):
        url = reverse('accounts-list')
        self.account_name = 'Test Checking'
        data = {'account_name': self.account_name, 'account_type': Accounts.CHECKING}
        self.setup_response = self.client.post(url, data, format='json')

    def test_create_account(self):
        """
        Verify we can create a new account

        Actual creation done in setup so its available for following tests
        """
        self.assertEqual(self.setup_response.status_code, status.HTTP_201_CREATED)
        account = Accounts.objects.get()
        self.assertEqual(Accounts.objects.count(), 1)
        self.assertEqual(account.account_name, self.account_name)
        self.assertEqual(account.account_type, Accounts.CHECKING)
        self.assertEqual(account.created_date, datetime.date.today())

    def test_update_account_name(self):
        """
        Verify we can patch the name of the account
        """
        account = Accounts.objects.get()
        url = reverse('accounts-detail', args=[account.id])
        new_account_name = 'Second Test Checking'
        data = {'account_name': new_account_name}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account = Accounts.objects.get()
        self.assertEqual(Accounts.objects.count(), 1)
        self.assertEqual(account.account_name, new_account_name)
        self.assertEqual(account.account_type, Accounts.CHECKING)
        self.assertEqual(account.created_date, datetime.date.today())

    def test_update_account_type(self):
        """
        Verify we can patch the type of the account
        """
        account = Accounts.objects.get()
        url = reverse('accounts-detail', args=[account.id])
        data = {'account_type': Accounts.SAVINGS}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account = Accounts.objects.get()
        self.assertEqual(Accounts.objects.count(), 1)
        self.assertEqual(account.account_name, self.account_name)
        self.assertEqual(account.account_type, Accounts.SAVINGS)
        self.assertEqual(account.created_date, datetime.date.today())

    def test_update_created_date(self):
        """
        Verify we can patch the create_date of the account but it doesn't actually change
        """
        account = Accounts.objects.get()
        url = reverse('accounts-detail', args=[account.id])
        date = datetime.date(2020, 1, 1)
        data = {'created_date': date}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account = Accounts.objects.get()
        self.assertEqual(Accounts.objects.count(), 1)
        self.assertEqual(account.account_name, self.account_name)
        self.assertEqual(account.account_type, Accounts.CHECKING)
        self.assertEqual(account.created_date, datetime.date.today())

    def test_update_all_fields(self):
        """
        Verify we can update the account_name and account_type with a put action
        """
        account = Accounts.objects.get()
        url = reverse('accounts-detail', args=[account.id])
        new_account_name = 'Savings'
        data = {'account_name': new_account_name, 'account_type': Accounts.SAVINGS}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account = Accounts.objects.get()
        self.assertEqual(Accounts.objects.count(), 1)
        self.assertEqual(account.account_name, new_account_name)
        self.assertEqual(account.account_type, Accounts.SAVINGS)
        self.assertEqual(account.created_date, datetime.date.today())

    def test_delete_account(self):
        """
        Verify we can delete the account
        """
        account = Accounts.objects.get()
        url = reverse('accounts-detail', args=[account.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Accounts.objects.count(), 0)

    def test_create_account_invalid_name(self):
        """
        Verify if create an account without a char value we get a 400 error
        """
        url = reverse('accounts-list')
        data = {'account_name': True, 'account_type': Accounts.CHECKING}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Accounts.objects.count(), 1)

    def test_create_account_name_too_long(self):
        """
        Verify if create an account with value to long we get an error
        """
        url = reverse('accounts-list')
        account_name = 'a' * 100
        data = {'account_name': account_name, 'account_type': Accounts.CHECKING}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Accounts.objects.count(), 1)

    def test_create_account_name_already_exists(self):
        """
        Verify if create an account with name that already exists we get an error
        """
        url = reverse('accounts-list')
        data = {'account_name': self.account_name, 'account_type': Accounts.CHECKING}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Accounts.objects.count(), 1)

    def test_create_account_invalid_account_type(self):
        """
        Verify if create an account with invalid type we get an error
        """
        url = reverse('accounts-list')
        data = {'account_name': 'Savings', 'account_type': 'foo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Accounts.objects.count(), 1)

    def test_update_account_name_invalid_name(self):
        """
        Verify if update an account without a char value we get a 400 error
        """
        account = Accounts.objects.get()
        url = reverse('accounts-detail', args=[account.id])
        data = {'account_name': True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Accounts.objects.count(), 1)

    def test_update_account_name_too_long(self):
        """
        Verify if patch account_name with value to long we get an error
        """
        account = Accounts.objects.get()
        url = reverse('accounts-detail', args=[account.id])
        account_name = 'a' * 100
        data = {'account_name': account_name}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_account_invalid_account_type(self):
        """
        Verify if patch an account with invalid type we get an error
        """
        account = Accounts.objects.get()
        url = reverse('accounts-detail', args=[account.id])
        data = {'account_type': 'foo'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_account_name_that_already_exists(self):
        """
        Verify if patch account_name with value that already exists we get an error
        """
        url = reverse('accounts-list')
        data = {'account_name': 'Savings', 'account_type': Accounts.SAVINGS}
        response = self.client.post(url, data, format='json')
        account = Accounts.objects.get(account_name='Savings')
        url = reverse('accounts-detail', args=[account.id])
        data = {'account_name': self.account_name}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
