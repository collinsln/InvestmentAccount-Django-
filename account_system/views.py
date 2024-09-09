from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from account_system.models import Transaction, UserAccount
from account_system.serializers import TransactionSerializer,TransactionSummarySerializer, TransactionDetailSerializer
from account_system.permissions import ViewOnlyPermission, FullAccessPermission, PostOnlyPermission
from account_system.models import Account


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
        
        # Filter the transactions by the account (account_pk) passed in the URL.
        
        account_pk = self.kwargs.get('account_pk')
        if account_pk:
            return self.queryset.filter(account_id=account_pk)
        return self.queryset
class UserTransactionSummaryView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = TransactionSummarySerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        account_id = kwargs.get('account_pk')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not account_id:
            return Response({"error": "Account ID is required"}, status=400)

        try:
            # Look for the account via UserAccount, not directly in Account
            user_account = UserAccount.objects.get(user=user, account_id=account_id)
            account = user_account.account
        except UserAccount.DoesNotExist:
            return Response({"error": "Account not found for this user"}, status=404)

        # Filter transactions associated with this account
        transactions = account.transaction_set.all()

        # Optionally filter by date if provided
        if start_date:
            start_date = parse_date(start_date)
            transactions = transactions.filter(date__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            transactions = transactions.filter(date__lte=end_date)

        # Serialize the account and its transactions
        serializer = TransactionSummarySerializer(account)
        data = serializer.data
        data['transactions'] = TransactionDetailSerializer(transactions, many=True).data
        return Response(data)
