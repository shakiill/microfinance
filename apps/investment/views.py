from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from apps.helpers.views import PageHeaderMixin
from apps.investment.filters import InvestmentFilterSet, DailySavingFilterSet
from apps.investment.forms import InvestmentAddForm, DailySavingAddForm
from apps.investment.models import Investment, DailySaving
from apps.investment.tables import InvestmentTable, DailySavingTable, DailySavingTransectionTable


# Create your views here.
class InvestmentAddView(PageHeaderMixin, LoginRequiredMixin, CreateView):
    permission_required = 'investment.add_investment'
    model = Investment
    form_class = InvestmentAddForm
    success_url = reverse_lazy('all_investments')
    template_name = 'add.html'
    page_title = 'Investment'
    list_link = reverse_lazy('all_investments')


class InvestmentListView(PageHeaderMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'investment.view_investment'
    model = Investment
    template_name = 'investment.html'
    paginate_by = 20
    ordering = '-id'
    table_class = InvestmentTable
    filterset_class = InvestmentFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Investment',
            'add_link': reverse_lazy('investment-add'),
            'filter': self.filterset
        })
        return context


def investment_update(request, pk):
    if request.method == 'POST':
        investment = Investment.objects.get(pk=pk)
        try:
            investment.number_of_shares = int(request.POST.get('number_of_shares'))
            investment.share_price = Decimal(request.POST.get('share_price'))
            investment.interest_rate = Decimal(request.POST.get('interest_rate'))
            investment.maturity_date = request.POST.get('maturity_date')
            investment.remarks = request.POST.get('remarks')

            # Record history before saving
            changes = {
                'number_of_shares': {'from': investment.number_of_shares,
                                     'to': int(request.POST.get('number_of_shares'))},
                'share_price': {'from': float(investment.share_price), 'to': float(request.POST.get('share_price'))},
                'interest_rate': {'from': float(investment.interest_rate),
                                  'to': float(request.POST.get('interest_rate'))},
                'maturity_date': {'from': str(investment.maturity_date), 'to': request.POST.get('maturity_date')},
                'remarks': {'from': investment.remarks, 'to': request.POST.get('remarks')},
                'changed_by': request.user.username
            }

            if not investment.history:
                investment.history = []

            investment.history.append({
                'timestamp': timezone.now().isoformat(),
                'action': 'updated',
                'user': request.user.username,
                'changes': changes
            })

            investment.save()
            messages.success(request, 'Investment updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating investment: {str(e)}')

        return redirect('all_investments')


def investment_delete(request, pk):
    if request.method == 'POST':
        investment = Investment.objects.get(pk=pk)
        try:
            # Record deletion in history before deleting
            if not investment.history:
                investment.history = []

            investment.history.append({
                'timestamp': timezone.now().isoformat(),
                'action': 'deleted',
                'user': request.user.username
            })

            investment.save()  # Save the history first
            investment.delete()
            messages.success(request, 'Investment deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting investment: {str(e)}')

        return redirect('all_investments')


class DailySavingAddView(PageHeaderMixin, LoginRequiredMixin, CreateView):
    permission_required = 'investment.add_daily_saving'
    model = DailySaving
    form_class = DailySavingAddForm
    success_url = reverse_lazy('daily-saving-list')
    template_name = 'add.html'
    page_title = 'Daily saving'
    list_link = reverse_lazy('daily-saving-list')


class DailySavingListView(PageHeaderMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'investment.view_daily_saving'
    model = DailySaving
    template_name = 'list.html'
    paginate_by = 20
    ordering = '-id'
    table_class = DailySavingTable
    filterset_class = DailySavingFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Daily saving',
            'add_link': reverse_lazy('daily-saving-add'),
            'filter': self.filterset
        })
        return context


class DailySavingTransactionView(PageHeaderMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'investment.view_daily_saving'
    model = DailySaving
    template_name = 'daily-savings.html'
    paginate_by = 20
    ordering = '-id'
    table_class = DailySavingTransectionTable
    filterset_class = DailySavingFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Daily saving transaction',
            'add_link': reverse_lazy('daily-saving-add'),
            'filter': self.filterset
        })
        return context
