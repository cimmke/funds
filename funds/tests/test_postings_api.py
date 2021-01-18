import datetime

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from funds.models import Postings


class PostingsAPITest(APITestCase):

    def setUp(self):
        url = reverse('postings-list')
        self.posting_num = 1
        self.payee = 'Store'
        self.note = 'Note'
        data = {
            'posting_num': self.posting_num,
            'posting_type': Postings.STANDARD,
            'payee': self.payee,
            'note': self.note
        }
        self.setup_response = self.client.post(url, data, format='json')

    def test_create_account(self):
        """
        Verify we can create a new posting

        Actual creation done in setup so its available for following tests
        """
        self.assertEqual(self.setup_response.status_code, status.HTTP_201_CREATED)
        posting = Postings.objects.get()
        self.assertEqual(Postings.objects.count(), 1)
        self.assertEqual(posting.posting_num, self.posting_num)
        self.assertEqual(posting.posting_type, Postings.STANDARD)
        self.assertEqual(posting.date, datetime.date.today())
        self.assertEqual(posting.payee, self.payee)
        self.assertFalse(posting.cleared)
        self.assertEqual(posting.note, self.note)

    def test_update_posting_date(self):
        """
        Verify we can patch the date of the posting
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        new_posting_date = datetime.date(2020, 12, 11)
        data = {'date': new_posting_date}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posting = Postings.objects.get()
        self.assertEqual(posting.posting_num, self.posting_num)
        self.assertEqual(posting.posting_type, Postings.STANDARD)
        self.assertEqual(posting.date, new_posting_date)
        self.assertEqual(posting.payee, self.payee)
        self.assertFalse(posting.cleared)
        self.assertEqual(posting.note, self.note)

    def test_update_posting_type(self):
        """
        Verify we can patch the type of the posting
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        data = {'posting_type': Postings.INCOME}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posting = Postings.objects.get()
        self.assertEqual(Postings.objects.count(), 1)
        self.assertEqual(posting.posting_num, self.posting_num)
        self.assertEqual(posting.posting_type, Postings.INCOME)
        self.assertEqual(posting.date, datetime.date.today())
        self.assertEqual(posting.payee, self.payee)
        self.assertFalse(posting.cleared)
        self.assertEqual(posting.note, self.note)

    def test_update_payee(self):
        """
        Verify we can patch the payee of the posting
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        new_payee = 'New Store'
        data = {'payee': new_payee}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posting = Postings.objects.get()
        self.assertEqual(Postings.objects.count(), 1)
        self.assertEqual(posting.posting_num, self.posting_num)
        self.assertEqual(posting.posting_type, Postings.STANDARD)
        self.assertEqual(posting.date, datetime.date.today())
        self.assertEqual(posting.payee, new_payee)
        self.assertFalse(posting.cleared)
        self.assertEqual(posting.note, self.note)

    def test_update_cleared(self):
        """
        Verify we can patch if the posting is cleared
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        data = {'cleared': True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posting = Postings.objects.get()
        self.assertEqual(Postings.objects.count(), 1)
        self.assertEqual(posting.posting_num, self.posting_num)
        self.assertEqual(posting.posting_type, Postings.STANDARD)
        self.assertEqual(posting.date, datetime.date.today())
        self.assertEqual(posting.payee, self.payee)
        self.assertTrue(posting.cleared)
        self.assertEqual(posting.note, self.note)

    def test_update_note(self):
        """
        Verify we can patch the note of the posting
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        new_note = 'New Note'
        data = {'note': new_note}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posting = Postings.objects.get()
        self.assertEqual(Postings.objects.count(), 1)
        self.assertEqual(posting.posting_num, self.posting_num)
        self.assertEqual(posting.posting_type, Postings.STANDARD)
        self.assertEqual(posting.date, datetime.date.today())
        self.assertEqual(posting.payee, self.payee)
        self.assertFalse(posting.cleared)
        self.assertEqual(posting.note, new_note)

    def test_update_all_fields(self):
        """
        Verify we can update all the fields with a put action
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        new_date = datetime.date(2020, 12, 11)
        new_payee = 'New Payee'
        new_note = 'New Note'
        data = {
            'posting_num': posting.posting_num,
            'posting_type': Postings.TRANSFER,
            'date': new_date,
            'payee': new_payee,
            'cleared': True,
            'note': new_note
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posting = Postings.objects.get()
        self.assertEqual(Postings.objects.count(), 1)
        self.assertEqual(posting.posting_num, self.posting_num)
        self.assertEqual(posting.posting_type, Postings.TRANSFER)
        self.assertEqual(posting.date, new_date)
        self.assertEqual(posting.payee, new_payee)
        self.assertTrue(posting.cleared)
        self.assertEqual(posting.note, new_note)

    def test_delete_posting(self):
        """
        Verify we can delete the posting
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Postings.objects.count(), 0)

    def test_create_posting_negative_num(self):
        """
        Verify if create a posting with a negative int we get a 400 error
        """
        url = reverse('postings-list')
        data = {
            'posting_num': -1,
            'posting_type': Postings.STANDARD,
            'payee': self.payee,
            'note': self.note
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Postings.objects.count(), 1)

    def test_create_posting_invalid_posting_type(self):
        """
        Verify if create a posting with invalid type we get an error
        """
        url = reverse('postings-list')
        data = {
            'posting_num': self.posting_num,
            'posting_type': 'Invalid',
            'payee': self.payee,
            'note': self.note
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Postings.objects.count(), 1)

    def test_create_posting_payee_too_long(self):
        """
        Verify if create an posting with payee to long we get an error
        """
        url = reverse('postings-list')
        payee = 'a' * 100
        data = {
            'posting_num': self.posting_num,
            'posting_type': Postings.STANDARD,
            'payee': payee,
            'note': self.note
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Postings.objects.count(), 1)

    def test_create_posting_payee_blank(self):
        """
        Verify can create a posting with a blank payee
        """
        url = reverse('postings-list')
        data = {
            'posting_num': self.posting_num + 1,
            'posting_type': Postings.STANDARD,
            'note': self.note
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        posting = Postings.objects.get(pk=2)
        self.assertEqual(Postings.objects.count(), 2)
        self.assertEqual(posting.posting_num, self.posting_num + 1)
        self.assertEqual(posting.posting_type, Postings.STANDARD)
        self.assertEqual(posting.date, datetime.date.today())
        self.assertEqual(posting.payee, '')
        self.assertFalse(posting.cleared)
        self.assertEqual(posting.note, self.note)

    def test_create_posting_note_blank(self):
        """
        Verify can create a posting with a blank note
        """
        url = reverse('postings-list')
        data = {
            'posting_num': self.posting_num + 1,
            'posting_type': Postings.STANDARD,
            'payee': self.payee
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        posting = Postings.objects.get(pk=2)
        self.assertEqual(Postings.objects.count(), 2)
        self.assertEqual(posting.posting_num, self.posting_num + 1)
        self.assertEqual(posting.posting_type, Postings.STANDARD)
        self.assertEqual(posting.date, datetime.date.today())
        self.assertEqual(posting.payee, self.payee)
        self.assertFalse(posting.cleared)
        self.assertEqual(posting.note, '')

    def test_create_posting_cleared_invalid_type(self):
        """
        Verify if create a posting with invalid type for cleared get 400 error
        """
        url = reverse('postings-list')
        cleared = 5
        data = {
            'posting_num': self.posting_num + 1,
            'posting_type': Postings.STANDARD,
            'payee': self.payee,
            'cleared': cleared,
            'note': self.note
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Postings.objects.count(), 1)

    def test_update_posting_date_blank(self):
        """
        Verify if update date with blank value get 400 error
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        new_date = ''
        data = {'date': new_date}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_posting_posting_type_invalid(self):
        """
        Verify if update posting_type with invalid value get 400 error
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        data = {'posting_type': 'Invalid'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_posting_payee_too_long(self):
        """
        Verify if update posting with value that is too long get 400 error
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        new_payee = 'a' * 100
        data = {'payee': new_payee}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_posting_cleared_invalid_type(self):
        """
        Verify if update posting with invalid type for cleared get 400 error
        """
        posting = Postings.objects.get()
        url = reverse('postings-detail', args=[posting.posting_num])
        data = {'cleared': 'a'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
