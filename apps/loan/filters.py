import django_filters
from django_filters.widgets import RangeWidget

from apps.loan.forms import LoanApplicationFilterForm, LoanFilterForm, RepaymentFilterForm, TransactionFilterForm, \
    LoanDisbursementTransactionFilterForm
from apps.loan.models import LoanApplication, Loan, Installment, Transaction, LoanDisbursementTransaction
from apps.user.models import CustomUser


class LoanApplicationFilterSet(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains')
    applied_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))
    approved_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))

    class Meta:
        model = LoanApplication
        fields = ['customer', 'status', 'applied_date', 'approved_date']
        form = LoanApplicationFilterForm


class LoanFilterSet(django_filters.FilterSet):
    disbursed_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))
    maturity_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))

    name = django_filters.CharFilter(lookup_expr='icontains', field_name='customer__name', label='Name')
    mobile = django_filters.CharFilter(lookup_expr='icontains', field_name='customer__mobile', label='Mobile Number')

    class Meta:
        model = Loan
        fields = ['status', 'disbursed_date', 'maturity_date']
        form = LoanFilterForm


class RepaymentFilterSet(django_filters.FilterSet):
    due_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))
    paid_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))
    assigned = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.filter(loans_assign_by__isnull=False).distinct(), label='Assigned To', field_name='loan__assign_by')
    name = django_filters.CharFilter(lookup_expr='icontains', field_name='loan__customer__name', label='Name')
    mobile = django_filters.CharFilter(lookup_expr='icontains', field_name='loan__customer__mobile',
                                       label='Mobile Number')

    class Meta:
        model = Installment
        fields = ['payment_status', 'due_date', 'paid_date']
        form = RepaymentFilterForm


class TransactiontFilterSet(django_filters.FilterSet):
    transaction_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))
    collected_by = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.filter(loans_assign_by__isnull=False).distinct(), label='Collected by')

    name = django_filters.CharFilter(lookup_expr='icontains', field_name='installment__loan__customer__name', label='Name')
    mobile = django_filters.CharFilter(lookup_expr='icontains', field_name='installment__loan__customer__mobile',
                                       label='Mobile Number')

    class Meta:
        model = Transaction
        fields = ['transaction_date', 'collected_by', 'status']
        form = TransactionFilterForm


class LoanDisbursementTransactionFilterSet(django_filters.FilterSet):
    transaction_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))
    name = django_filters.CharFilter(lookup_expr='icontains', field_name='disbursed_to__name',
                                     label='Customer Name')
    mobile = django_filters.CharFilter(lookup_expr='icontains', field_name='disbursed_to__mobile',
                                       label='Mobile Number')
    loan_id = django_filters.CharFilter(lookup_expr='exact', field_name='loan__loan_application__id',
                                        label='Loan ID')
    amount = django_filters.RangeFilter(widget=RangeWidget(attrs={'class': 'date-range'}))

    class Meta:
        model = LoanDisbursementTransaction
        fields = ['transaction_date', 'amount']
        form = LoanDisbursementTransactionFilterForm
