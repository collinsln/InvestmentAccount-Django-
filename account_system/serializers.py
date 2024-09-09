from rest_framework import serializers
from account_system.models import Account, Transaction, UserAccount

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id','account', 'amount', 'date', 'created_at']

class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    total_balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'name', 'created_at', 'transactions', 'total_balance']

    def get_total_balance(self, obj):
        transactions = obj.transaction_set.all()
        return sum(transaction.amount for transaction in transactions)

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['user', 'account', 'account_type']

from rest_framework import serializers
from account_system.models import Account, Transaction

class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'date', 'description']

class TransactionSummarySerializer(serializers.ModelSerializer):
    transactions = TransactionDetailSerializer(many=True, read_only=True)
    total_balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'created_at', 'transactions', 'total_balance']

    def get_total_balance(self, obj):
        # Calculate the total balance based on the transactions
        total_balance = obj.balance + sum([t.amount for t in obj.transaction_set.all()])
        return total_balance