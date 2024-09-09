from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account_system.views import UserAccountViewSet,TransactionViewSet, UserTransactionSummaryView, AccountViewSet, UserViewSet

# from django.contrib import admin #for django admin panl

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'accounts/(?P<account_pk>\d+)/transactions', TransactionViewSet, basename='transaction')
router.register(r'users', UserViewSet, basename='user')
router.register(r'user_accounts', UserAccountViewSet, basename='user-account')

# I should add url prefix hapa
urlpatterns = [
    # path('admin/', admin.site.urls),  #for django admin panel. not working now conflict with admin url
    path('', include(router.urls)),  # viewset URLs
    path('admin/accounts/<int:account_pk>/transactions/', UserTransactionSummaryView.as_view(), name='user-transaction-summary'),
   
    ]

