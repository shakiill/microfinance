import django_filters
from django_filters.widgets import RangeWidget

from apps.investment.forms import InvestmentFilterForm
from apps.investment.models import Investment


class InvestmentFilterSet(django_filters.FilterSet):
    investment_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))
    maturity_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))
    amount = django_filters.RangeFilter(widget=RangeWidget(attrs={'class': 'date-range'}))

    class Meta:
        model = Investment
        fields = ['customer', 'amount', 'status', 'investment_date', 'maturity_date']
        form = InvestmentFilterForm
