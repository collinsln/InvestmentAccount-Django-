from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=50)  # view_only, full_access, post_only

    class Meta:
        unique_together = ('user', 'account')

    def __str__(self):
        return f'{self.user.username} - {self.account.name} ({self.account_type})'

class Account(models.Model):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255) 

    def __str__(self):
        return f'{self.account.name} - {self.amount:.2f} on {self.date}'
