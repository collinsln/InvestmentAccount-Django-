from django.urls import reverse
from rest_framework.test import APIClient
from django.utils import timezone
from django.test import TestCase
from account_system.models import Account, UserAccount, Transaction
from django.contrib.auth.models import User

class AccountPostOnlyPermissionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='postonlyuser', password='12345')
        self.account = Account.objects.create(name='Post Only Account', balance=1000)
        self.user_account = UserAccount.objects.create(user=self.user, account=self.account, account_type='post_only')
        self.client.login(username='postonlyuser', password='12345')

    def test_post_only_permissions(self):
        url = reverse('transaction-list', kwargs={'account_pk': self.account.id})

       
        response = self.client.post(url, {
            'amount': 50,
            'description': 'New Post-Only Transaction',
            'date': timezone.now().date(),
            'account': self.account.id  
        })

       
        print("POST response status code:", response.status_code) # Debug output is it
        print("POST response content:", response.content)

        self.assertEqual(response.status_code, 201)

        # Check kama hiyo transaction created successfully and retrieve its ID
        transaction_id = response.data.get('id')
        self.assertIsNotNone(transaction_id, "Transaction ID should not be None after creation.")

        # Test ku_Read 
        response = self.client.get(url)

        
        print("GET response status code:", response.status_code)# Debug output just like the above
        print("GET response content:", response.content)

        self.assertEqual(response.status_code, 403) #should fail for post-only users

        # Test ya ku_Update 
        update_url = reverse('transaction-detail', kwargs={'account_pk': self.account.id, 'pk': transaction_id})
        response = self.client.put(update_url, {
            'amount': 75,
            'description': 'Updated Post-Only Transaction',
            'date': timezone.now().date(),
            'account': self.account.id  # Include the account field
        })

        # Debug print
        print("PUT response status code:", response.status_code)
        print("PUT response content:", response.content)

        self.assertEqual(response.status_code, 403) #should fail for post-only users

        # Test ku_Delete 
        response = self.client.delete(update_url)

        # Debugging output
        print("DELETE response status code:", response.status_code)
        print("DELETE response content:", response.content)

        self.assertEqual(response.status_code, 403)#should fail for post-only users
