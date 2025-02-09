import django_filters
from django_filters.widgets import RangeWidget

from apps.loan.forms import LoanApplicationFilterForm
from apps.loan.models import LoanApplication, Loan


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
        form = LoanApplicationFilterForm
