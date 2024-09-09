from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.utils import timezone
from django.test import TestCase
from account_system.models import Account, Transaction, UserAccount

class AdminTransactionSummaryTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create an admin user and a regular user
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.regular_user = User.objects.create_user(username='user', password='userpass')

        # Create an account
        self.account = Account.objects.create(name='Test Account', balance=1000)

        # Link the admin user to the account with full access
        UserAccount.objects.create(user=self.admin_user, account=self.account, account_type='full_access')

        # Create some transactions
        self.transactions = [
            Transaction.objects.create(account=self.account, amount=100, date=timezone.now().date(), description="Test transaction 1"),
            Transaction.objects.create(account=self.account, amount=200, date=timezone.now().date(), description="Test transaction 2")
        ]

    def test_admin_access(self):
        # Log in as admin user
        self.client.login(username='admin', password='adminpass')
        url = f'/admin/accounts/{self.account.id}/transactions/'
        response = self.client.get(url)

        print(f"Admin access response status code: {response.status_code}")
        print(f"Admin access response data: {response.data}")

        self.assertEqual(response.status_code, 200)
        self.assertIn('total_balance', response.data)
        self.assertIn('transactions', response.data)

    def test_non_admin_access(self):
        # Log in as regular user
        self.client.login(username='user', password='userpass')
        url = f'/admin/accounts/{self.account.id}/transactions/'
        response = self.client.get(url)

        print(f"Non-admin access response status code: {response.status_code}")
        print(f"Non-admin access response data: {response.data}")

        self.assertEqual(response.status_code, 403)
