from rest_framework import generics

from api.user.serializers import TransactionSerializer, InstallmentSerializer, DailySavingSerializer, \
    WithdrawalSerializer
from apps.investment.models import DailySaving, Withdrawal
from apps.loan.models import Installment, Transaction


class CustomerTransactionsListView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Transaction.objects.filter(installment__loan__customer__id=customer_id).select_related(
            'installment', 'installment__loan', 'collected_by'
        )


class CustomerInstallmentsListView(generics.ListAPIView):
    serializer_class = InstallmentSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Installment.objects.filter(loan__customer__id=customer_id).select_related('loan')


class CustomerSavingsListView(generics.ListAPIView):
    serializer_class = DailySavingSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        # Include both savings and withdrawals in the same endpoint
        savings = DailySaving.objects.filter(customer__id=customer_id).select_related('collected_by')
        return savings


class CustomerWithdrawalsListView(generics.ListAPIView):
    serializer_class = WithdrawalSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Withdrawal.objects.filter(customer__id=customer_id).select_related('collected_by')
