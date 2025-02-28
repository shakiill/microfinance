from rest_framework import serializers

from apps.investment.models import DailySaving, Withdrawal
from apps.loan.models import LoanApplication, Installment, Transaction


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ['id', 'amount', 'duration_months', 'purpose', 'status', 'applied_date',
                  'approved_date', 'disbursed_date']


class InstallmentSerializer(serializers.ModelSerializer):
    loan_id = serializers.IntegerField(source='loan.id', read_only=True)

    class Meta:
        model = Installment
        fields = ['id', 'loan_id', 'interest_amount', 'principal_amount', 'amount',
                  'paid_amount', 'due_date', 'paid_date', 'payment_status']


class TransactionSerializer(serializers.ModelSerializer):
    installment_id = serializers.IntegerField(source='installment.id', read_only=True)
    loan_id = serializers.IntegerField(source='installment.loan.id', read_only=True)
    collected_by_name = serializers.CharField(source='collected_by.username', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'installment_id', 'loan_id', 'amount', 'transaction_date',
                  'transaction_type', 'status', 'collected_by_name', 'remarks']


class DailySavingSerializer(serializers.ModelSerializer):
    collected_by_name = serializers.CharField(source='collected_by.username', read_only=True)

    class Meta:
        model = DailySaving
        fields = ['id', 'amount', 'date', 'saving_type', 'status', 'collected_by_name', 'remarks']


class WithdrawalSerializer(serializers.ModelSerializer):
    collected_by_name = serializers.CharField(source='collected_by.username', read_only=True)

    class Meta:
        model = Withdrawal
        fields = ['id', 'amount', 'date', 'collected_by_name', 'remarks']
