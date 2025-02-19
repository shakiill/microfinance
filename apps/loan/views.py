from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from decimal import Decimal

from apps.helpers.views import PageHeaderMixin
from apps.loan.filters import LoanApplicationFilterSet, LoanFilterSet, RepaymentFilterSet
from apps.loan.forms import LoanApplicationForm
from apps.loan.models import LoanApplication, ApplicationProduct, Guarantor, Asset, FinancialRecord, CheckInfo, \
    LoanStatusHistory, Loan, LoanDisbursementTransaction, Installment, Transaction
from apps.loan.tables import LoanApplicationTable, LoanTable, RepaymentTable
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
        context['installments'] = Installment.objects.filter(loan=self.object).order_by('due_date')
        context['disbursement_transaction'] = LoanDisbursementTransaction.objects.filter(loan=self.object)
        return context


def installment_details(request, installment_id):
    installment = get_object_or_404(Installment, id=installment_id)
    transactions = installment.transactions.all()

    data = {
        'installment_id': installment.id,
        'due_date': installment.due_date,
        'principal': installment.principal_amount,
        'interest': installment.interest_amount,
        'total_amount': installment.amount,
        'paid_amount': installment.paid_amount,
        'remaining_amount': installment.amount - installment.paid_amount,
        'payment_status': installment.payment_status,
        'payment_timing': installment.payment_timing,
        'transactions': []
    }

    for transaction in transactions:
        data['transactions'].append({
            'id': transaction.id,
            'date': transaction.transaction_date,
            'amount': transaction.amount,
            'type': transaction.transaction_type,
            'collected_by': transaction.collected_by.name if transaction.collected_by else '',
            'remarks': transaction.remarks or '',
        })

    return JsonResponse(data)


class RepaymentListView(PageHeaderMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'loan.view_installment'
    model = Installment
    template_name = 'repayments.html'
    paginate_by = 10
    ordering = '-due_date'
    table_class = RepaymentTable
    filterset_class = RepaymentFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Repayments',
            # 'add_link': reverse_lazy('user_add'),
            'filter': self.filterset
        })
        return context


@login_required
def get_transaction_history(request, installment_id):
    transactions = Transaction.objects.filter(installment_id=installment_id) \
        .select_related('collected_by', 'verified_by') \
        .order_by('-transaction_date')

    data = [{
        'date': t.transaction_date.strftime('%Y-%m-%d'),
        'amount': float(t.amount),
        'type': t.transaction_type,
        'collected_by': t.collected_by.get_full_name() if t.collected_by else '-',
        'verified_by': t.verified_by.get_full_name() if t.verified_by else '-',
        'remarks': t.remarks or '-'
    } for t in transactions]

    return JsonResponse({'transactions': data})


@require_POST
@login_required
def create_transaction(request):
    try:
        installment_id = request.POST.get('installment_id')
        amount = Decimal(request.POST.get('amount', '0'))  # Convert to Decimal
        transaction_date = request.POST.get('transaction_date')
        remarks = request.POST.get('remarks')

        installment = Installment.objects.get(id=installment_id)

        # Optional: Add validation
        remaining_amount = installment.amount - installment.paid_amount
        if amount > remaining_amount:
            return JsonResponse({
                'status': 'error',
                'message': f'Payment amount cannot exceed remaining balance of {remaining_amount}'
            }, status=400)

        transaction = Transaction.objects.create(
            installment=installment,
            amount=amount,
            transaction_date=transaction_date,
            transaction_type=Transaction.TransactionTypeChoices.PAYMENT,
            remarks=remarks,
            created_by=request.user,
            collected_by=request.user
        )

        # Refresh installment to get updated paid_amount
        installment.refresh_from_db()

        return JsonResponse({
            'status': 'success',
            'message': 'Payment recorded successfully',
            'new_paid_amount': float(installment.paid_amount),
            'new_status': installment.payment_status
        })
    except ValueError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid amount provided'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)