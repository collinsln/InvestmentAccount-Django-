from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account_system.views import TransactionViewSet

router = DefaultRouter()
router.register(r'accounts/(?P<account_pk>\d+)/transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]
