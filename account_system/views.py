from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from account_system.models import Transaction, UserAccount
from account_system.serializers import TransactionSerializer
from account_system.permissions import ViewOnlyPermission, FullAccessPermission, PostOnlyPermission

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_permissions(self):
        """
        Return the permission classes based on user access type.
        """
        if self.request.user.is_authenticated:
            account_id = self.kwargs.get('account_pk')
            if account_id:
                try:
                    user_account = UserAccount.objects.get(user=self.request.user, account_id=account_id)
                    if user_account.account_type == 'full_access':
                        return [IsAuthenticated(), FullAccessPermission()]
                    elif user_account.account_type == 'post_only':
                        if self.request.method == 'POST':
                            return [IsAuthenticated(), PostOnlyPermission()]
                        # Deny access for GET, PUT, DELETE for 'post_only' users
                        return [IsAuthenticated(), PostOnlyPermission()]
                except UserAccount.DoesNotExist:
                    pass

        # Default to view only permission if no specific permissions match
        return [IsAuthenticated(), ViewOnlyPermission()]

    def get_queryset(self):
        """
        Filter the transactions by the account (account_pk) passed in the URL.
        """
        account_pk = self.kwargs.get('account_pk')
        if account_pk:
            return self.queryset.filter(account_id=account_pk)
        return self.queryset
