import django_filters
from django_filters.widgets import RangeWidget

from apps.loan.forms import LoanApplicationFilterForm
from apps.loan.models import LoanApplication


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
