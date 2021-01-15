import datetime

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from funds.models import Categories


class CategoriesAPITest(APITestCase):

    def setUp(self):
        url = reverse('categories-list')
        self.category_name = 'Test Category'
        data = {'category_name': self.category_name}
        self.setup_response = self.client.post(url, data, format='json')

    def test_create_category(self):
        """
        Verify we can create a new category

        Actual creation done in setup so its available for following tests
        """
        self.assertEqual(self.setup_response.status_code, status.HTTP_201_CREATED)
        category = Categories.objects.get()
        self.assertEqual(Categories.objects.count(), 1)
        self.assertEqual(category.category_name, self.category_name)
        self.assertEqual(category.created_date, datetime.date.today())

    def test_update_category_name(self):
        """
        Verify we can patch the name of the account
        """
        category = Categories.objects.get()
        url = reverse('categories-detail', args=[category.id])
        new_category_name = 'Second Test Category'
        data = {'category_name': new_category_name}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category = Categories.objects.get()
        self.assertEqual(Categories.objects.count(), 1)
        self.assertEqual(category.category_name, new_category_name)
        self.assertEqual(category.created_date, datetime.date.today())

    def test_update_created_date(self):
        """
        Verify we can patch the create_date of the category but doesn't actually change
        """
        category = Categories.objects.get()
        url = reverse('categories-detail', args=[category.id])
        date = datetime.date(2020, 1, 1)
        data = {'created_date': date}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category = Categories.objects.get()
        self.assertEqual(Categories.objects.count(), 1)
        self.assertEqual(category.category_name, self.category_name)
        self.assertEqual(category.created_date, datetime.date.today())

    def test_update_all_fields(self):
        """
        Verify we can update the category_name with a put action
        """
        category = Categories.objects.get()
        url = reverse('categories-detail', args=[category.id])
        new_category_name = 'Other name'
        data = {'category_name': new_category_name}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category = Categories.objects.get()
        self.assertEqual(Categories.objects.count(), 1)
        self.assertEqual(category.category_name, new_category_name)
        self.assertEqual(category.created_date, datetime.date.today())

    def test_delete_category(self):
        """
        Verify we can delete the category
        """
        category = Categories.objects.get()
        url = reverse('categories-detail', args=[category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Categories.objects.count(), 0)

    def test_create_category_invalid_name(self):
        """
        Verify if create a category without a char value we get a 400 error
        """
        url = reverse('categories-list')
        data = {'category_name': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Categories.objects.count(), 1)

    def test_create_category_name_too_long(self):
        """
        Verify if create a category with value to long we get an error
        """
        url = reverse('categories-list')
        category_name = 'a' * 100
        data = {'category_name': category_name}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Categories.objects.count(), 1)

    def test_create_category_name_already_exists(self):
        """
        Verify if create a category with name that already exists we get an error
        """
        url = reverse('categories-list')
        data = {'category_name': self.category_name}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Categories.objects.count(), 1)

    def test_update_category_name_invalid_name(self):
        """
        Verify if update an category without a char value we get a 400 error
        """
        category = Categories.objects.get()
        url = reverse('categories-detail', args=[category.id])
        data = {'category_name': True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Categories.objects.count(), 1)

    def test_update_category_name_too_long(self):
        """
        Verify if patch category_name with value to long we get an error
        """
        category = Categories.objects.get()
        url = reverse('categories-detail', args=[category.id])
        category_name = 'a' * 100
        data = {'category_name': category_name}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_category_name_that_already_exists(self):
        """
        Verify if patch category_name with value that already exists we get an error
        """
        url = reverse('categories-list')
        data = {'category_name': 'Test'}
        response = self.client.post(url, data, format='json')
        category = Categories.objects.get(category_name='Test')
        url = reverse('categories-detail', args=[category.id])
        data = {'category_name': self.category_name}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
