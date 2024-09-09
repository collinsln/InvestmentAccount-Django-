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
        self.user_account = UserAccount.objects.create(user=self.user, account=self.account, account_type='view_only')
        
        # Create a Transaction object with a date
        self.transaction = Transaction.objects.create(
            account=self.account, 
            amount=100, 
            description='Test Transaction', 
            date=timezone.now()  # Adding date field
        )

        self.client.login(username='testuser', password='12345')

    def test_view_only_permission(self):
        url = reverse('transaction-list', kwargs={'account_pk': self.account.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Test non-safe method (e.g., POST)
        response = self.client.post(url, {'amount': 50, 'description': 'New Transaction'})
        self.assertEqual(response.status_code, 403)
