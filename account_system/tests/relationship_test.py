from django.test import TestCase
from django.contrib.auth.models import User
from account_system.models import Account, Transaction, UserAccount

class UserAccountModelTest(TestCase):
    def setUp(self):
        # Create users and accounts
        self.user = User.objects.create_user(username='testuser', password='password')
        self.account = Account.objects.create(name='Test Account')
        self.user_account = UserAccount.objects.create(
            user=self.user,
            account=self.account,
            account_type='view_only'
        )

    def test_user_account_association(self):
        """Test that UserAccount correctly associates User and Account."""
        user_account = UserAccount.objects.get(user=self.user, account=self.account)
        self.assertEqual(user_account.user, self.user)
        self.assertEqual(user_account.account, self.account)
        self.assertEqual(user_account.account_type, 'view_only')

    def test_user_accounts_retrieval(self):
        """Test that accounts are correctly retrieved for a user."""
        self.account2 = Account.objects.create(name='Account 2')
        UserAccount.objects.create(user=self.user, account=self.account2, account_type='full_access')

        user_accounts = UserAccount.objects.filter(user=self.user)
        self.assertEqual(user_accounts.count(), 2)
        accounts = [ua.account for ua in user_accounts]
        self.assertIn(self.account, accounts)
        self.assertIn(self.account2, accounts)

class TransactionAccessTest(TestCase):
    def setUp(self):
        # Create users, accounts, and transactions
        self.user = User.objects.create_user(username='testuser', password='password')
        self.account = Account.objects.create(name='Test Account')
        self.transaction = Transaction.objects.create(
            account=self.account,
            amount=100.0,
            date='2024-09-08'
        )
        UserAccount.objects.create(user=self.user, account=self.account, account_type='full_access')

    def test_user_access_to_transaction(self):
        """Test that transactions for an account are accessible by a user with the correct relationship."""
        user_accounts = UserAccount.objects.filter(user=self.user)
        account_ids = [ua.account.id for ua in user_accounts]
        transactions = Transaction.objects.filter(account__id__in=account_ids)
        self.assertIn(self.transaction, transactions)
