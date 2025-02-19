import django_filters
from django_filters.widgets import RangeWidget

from apps.loan.forms import LoanApplicationFilterForm, LoanFilterForm, RepaymentFilterForm
from apps.loan.models import LoanApplication, Loan, Installment
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
