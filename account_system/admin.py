# Hii page aint compulsory if you not using Django admin panel
from django.contrib import admin
from .models import Account, Transaction, UserAccount
from django.http import HttpResponse
import csv

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'date', 'created_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        user_accounts = UserAccount.objects.filter(user=user)
        accounts = [ua.account for ua in user_accounts]
        return qs.filter(account__in=accounts)

    def export_as_csv(self, request, queryset):
        # Generate a text response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=transactions.csv'
        writer = csv.writer(response)
        writer.writerow(['Account', 'Amount', 'Date', 'Created At'])
        for transaction in queryset:
            writer.writerow([transaction.account.name, transaction.amount, transaction.date, transaction.created_at])
        return response
    export_as_csv.short_description = 'Export selected transactions as CSV'

    actions = [export_as_csv]

admin.site.register(Account)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UserAccount)
