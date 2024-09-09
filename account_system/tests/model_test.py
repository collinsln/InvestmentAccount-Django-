from django.test import TestCase
from django.contrib.auth.models import User
from account_system.models import Account, Transaction, UserAccount

class AccountModelTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(name='Test Account')

    def test_account_creation(self):
        """Test creation of Account instance."""
        self.assertTrue(isinstance(self.account, Account))
        self.assertEqual(self.account.name, 'Test Account')
        self.assertEqual(Account.objects.count(), 1)

    def test_account_str(self):
        """Test the string representation of the Account model."""
        self.assertEqual(str(self.account), 'Test Account')

class UserAccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.account = Account.objects.create(name='Test Account')
        self.user_account = UserAccount.objects.create(user=self.user, account=self.account, account_type='view_only')

    def test_user_account_creation(self):
        """Test creation of UserAccount instance."""
        self.assertTrue(isinstance(self.user_account, UserAccount))
        self.assertEqual(self.user_account.user, self.user)
        self.assertEqual(self.user_account.account, self.account)
        self.assertEqual(self.user_account.account_type, 'view_only')
        self.assertEqual(UserAccount.objects.count(), 1)

    def test_user_account_unique_together(self):
        """Test unique_together constraint for UserAccount model."""
        with self.assertRaises(Exception):
            UserAccount.objects.create(user=self.user, account=self.account, account_type='post_only')

    def test_user_account_str(self):
        """Test the string representation of the UserAccount model."""
        self.assertEqual(str(self.user_account), f'{self.user.username} - {self.account.name} ({self.user_account.account_type})')

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.account = Account.objects.create(name='Test Account')
        self.transaction = Transaction.objects.create(account=self.account, amount=100.0, date='2024-09-08')

    def test_transaction_creation(self):
        """Test creation of Transaction instance."""
        self.assertTrue(isinstance(self.transaction, Transaction))
        self.assertEqual(self.transaction.account, self.account)
        self.assertEqual(self.transaction.amount, 100.0)
        self.assertEqual(self.transaction.date, '2024-09-08')
        self.assertEqual(Transaction.objects.count(), 1)

    def test_transaction_str(self):
        """Test the string representation of the Transaction model."""
        self.assertEqual(str(self.transaction), f'{self.account.name} - 100.00 on 2024-09-08')
