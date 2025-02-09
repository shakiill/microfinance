from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from apps.helpers.views import PageHeaderMixin
from apps.loan.filters import LoanApplicationFilterSet, LoanFilterSet
from apps.loan.forms import LoanApplicationForm
from apps.loan.models import LoanApplication, ApplicationProduct, Guarantor, Asset, FinancialRecord, CheckInfo, \
    LoanStatusHistory, Loan, LoanDisbursementTransaction, Installment, Transaction
from apps.loan.tables import LoanApplicationTable, LoanTable
from apps.user.models import CustomUser


# Create your views here.
class ApplicationListView(PageHeaderMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'loan.view_loanapplication'
    model = LoanApplication
    template_name = 'list.html'
    paginate_by = 10
    ordering = '-id'
    table_class = LoanApplicationTable
    filterset_class = LoanApplicationFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Applications',
            'add_link': reverse_lazy('user_add'),
            'filter': self.filterset
        })
        return context


class LoanListView(PageHeaderMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'loan.view_loan'
    model = Loan
    template_name = 'list.html'
    paginate_by = 10
    ordering = '-created_at'
    table_class = LoanTable
    filterset_class = LoanFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Disbursed Loans',
            # 'add_link': reverse_lazy('user_add'),
            'filter': self.filterset
        })
        return context


class LoanApplicationView(CreateView):
    model = LoanApplication
    form_class = LoanApplicationForm
    template_name = 'loan_add.html'

    def get_success_url(self):
        return reverse('loan_kyc', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super(LoanApplicationView, self).get_form_kwargs()
        pk = self.kwargs.get('pk')  # Get the user ID from the URL
        kwargs.update({'user': pk})  # Pass the user ID as a keyword argument
        return kwargs


class LoanKYCView(DetailView):
    model = LoanApplication
    template_name = 'kyc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ApplicationProduct.objects.filter(loan_application=self.object)
        context['guarantors'] = Guarantor.objects.filter(loan_application=self.object)
        context['assets'] = Asset.objects.filter(loan_application=self.object)
        context['financials'] = FinancialRecord.objects.filter(loan_application=self.object)
        context['checks'] = CheckInfo.objects.filter(loan_application=self.object)
        return context


class LoanApplicationDetailsView(DetailView):
    model = LoanApplication
    template_name = 'application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.object.customer
        context['products'] = ApplicationProduct.objects.filter(loan_application=self.object)
        context['total_price'] = context['products'].aggregate(total_price=Sum('total_price'))['total_price']
        context['guarantors'] = Guarantor.objects.filter(loan_application=self.object)
        context['assets'] = Asset.objects.filter(loan_application=self.object)
        context['financials'] = FinancialRecord.objects.filter(loan_application=self.object)
        context['checks'] = CheckInfo.objects.filter(loan_application=self.object)
        context['assign_by_list'] = CustomUser.objects.all()
        return context


# views.py
from django.utils import timezone


class LoanStatusChangeView(View):
    def post(self, request, pk):
        loan = get_object_or_404(LoanApplication, pk=pk)
        new_status = request.POST.get('status')
        remarks = request.POST.get('remarks')

        disburse_loan = Loan.objects.filter(loan_application=loan.pk)

        if disburse_loan:
            return JsonResponse(
                {'status': 'error', 'message': 'This application is already sanctioned! Status will not be changed.'},
                status=400)

        if new_status in dict(LoanApplication._meta.get_field('status').choices):
            # Save old status for history
            old_status = loan.status

            # Update loan status
            loan.status = new_status
            if new_status == 'APPROVED':
                loan.approved_date = timezone.now()
            elif new_status == 'DISBURSED':
                loan.disbursed_date = timezone.now()
            loan.save()

            # Create status history entry
            LoanStatusHistory.objects.create(
                loan=loan,
                from_status=old_status,
                to_status=new_status,
                changed_by=request.user,
                remarks=remarks
            )

            return JsonResponse({
                'status': 'success',
                'new_status': new_status,
                'changed_by': request.user.name,
                'changed_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)


class LoanDetailsView(DetailView):
    model = Loan
    template_name = 'loans.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.object.customer
        context['installments'] = Installment.objects.filter(loan=self.object)
        context['disbursement_transaction'] = LoanDisbursementTransaction.objects.filter(loan=self.object)
        return context
