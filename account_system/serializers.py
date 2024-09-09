from rest_framework import serializers
from account_system.models import Account, Transaction, UserAccount
from django.contrib.auth.models import User
from account_system.models import UserAccount

# user_account serializer url ya kucreate user and make them to belong tpo certain account
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'user', 'account', 'account_type']

        # ni ya user creation url
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

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