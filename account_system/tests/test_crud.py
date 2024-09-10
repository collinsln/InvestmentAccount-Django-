from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIClient
from account_system.models import Transaction, Account, UserAccount
from django.contrib.auth.models import User

class AccountPermissionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.account = Account.objects.create(name='Test Account', balance=1000)
        self.user_account = UserAccount.objects.create(user=self.user, account=self.account, account_type='full_access')
        self.client.login(username='testuser', password='12345')

    def test_full_access_permissions(self):
        #If i can creat C
        url = reverse('transaction-list', kwargs={'account_pk': self.account.id})
        response = self.client.post(url, {
            'amount': 50,
            'description': 'New Transaction',
            'date': timezone.now().date(),
            'account': self.account.id
        })
        print('Create Response:', response.data)  # Debugging
        self.assertEqual(response.status_code, 201)

        # If Read is possible R
        response = self.client.get(url)
        print('Read Response:', response.data)  # jsut a debug line
        self.assertEqual(response.status_code, 200)

        # test for Update U
        if response.status_code == 200 and len(response.data) > 0:
            # Accessing the first transaction in the response data
            transaction_id = response.data[0].get('id') if isinstance(response.data, list) else response.data.get('id')
            if not transaction_id:
                self.fail('Transaction ID is missing in the response data')
            update_url = reverse('transaction-detail', kwargs={'account_pk': self.account.id, 'pk': transaction_id})
            response = self.client.put(update_url, {
                'amount': 75,
                'description': 'Updated Transaction',
                'date': timezone.now().date(),
                'account': self.account.id
            })
            print('Update Response:', response.data)  # Debug respponse
            self.assertEqual(response.status_code, 200)
        else:
            self.fail('No transactions available to update')

        # If i can Delete D
        if response.status_code == 200 and len(response.data) > 0:
            transaction_id = response.data[0].get('id') if isinstance(response.data, list) else response.data.get('id')
            if not transaction_id:
                self.fail('Transaction ID is missing in the response data')
            delete_url = reverse('transaction-detail', kwargs={'account_pk': self.account.id, 'pk': transaction_id})
            response = self.client.delete(delete_url)
            self.assertEqual(response.status_code, 204)
        else:
            self.fail('No transactions available to delete')
