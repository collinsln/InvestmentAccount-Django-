from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.utils import timezone
from django.test import TestCase
from account_system.models import Account, Transaction, UserAccount

class AdminTransactionSummaryTest(TestCase):
    def setUp(self):
        self.client = APIClient()

       
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')#create admin
        self.regular_user = User.objects.create_user(username='user', password='userpass')#create normal user

        # Create an account
        self.account = Account.objects.create(name='Test Account', balance=1000)

        # Link make admin kuwa na full account with full access
        UserAccount.objects.create(user=self.admin_user, account=self.account, account_type='full_access')

        # Test transactions
        self.transactions = [
            Transaction.objects.create(account=self.account, amount=100, date=timezone.now().date(), description="Test transaction 1"),
            Transaction.objects.create(account=self.account, amount=200, date=timezone.now().date(), description="Test transaction 2")
        ]
# this class test kaa admin can log in
    def test_admin_access(self):
       
        self.client.login(username='admin', password='adminpass')
        url = f'/admin/accounts/{self.account.id}/transactions/'
        response = self.client.get(url)

        print(f"Admin access response status code: {response.status_code}")#if login is allowed
        print(f"Admin access response data: {response.data}")

        self.assertEqual(response.status_code, 200)
        self.assertIn('total_balance', response.data)
        self.assertIn('transactions', response.data)
 # Log in as regular user sio admin
    def test_non_admin_access(self):
    
        self.client.login(username='user', password='userpass')
        url = f'/admin/accounts/{self.account.id}/transactions/'
        response = self.client.get(url)

        print(f"Non-admin access response status code: {response.status_code}")
        print(f"Non-admin access response data: {response.data}")

        self.assertEqual(response.status_code, 403)
