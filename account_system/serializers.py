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
