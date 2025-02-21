from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from apps.helpers.views import PageHeaderMixin
from apps.investment.filters import InvestmentFilterSet
from apps.investment.models import Investment
from apps.investment.tables import InvestmentTable


# Create your views here.
class InvestmentListView(PageHeaderMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'investment.view_investment'
    model = Investment
    template_name = 'list.html'
    paginate_by = 20
    ordering = '-id'
    table_class = InvestmentTable
    filterset_class = InvestmentFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Investment',
            'add_link': reverse_lazy('user_add'),
            'filter': self.filterset
        })
        return context
