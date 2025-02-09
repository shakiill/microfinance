from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from datetime import datetime

from apps.loan.models import LoanDisbursementTransaction, Loan


@login_required
@require_POST
def create_disbursement(request, loan_id):
    try:
        loan = get_object_or_404(Loan, id=loan_id)

        # Create the disbursement transaction
        disbursement = LoanDisbursementTransaction(
            loan=loan,
            amount=Decimal(request.POST.get('amount')),
            transaction_date=datetime.strptime(request.POST.get('transaction_date'), '%Y-%m-%d').date(),
            remarks=request.POST.get('remarks'),
            disbursed_to=loan.customer,
            created_by=request.user,
            updated_by=request.user
        )

        # Save the disbursement
        disbursement.save()

        return JsonResponse({
            'success': True,
            'disbursement_id': disbursement.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@require_POST
def update_disbursement(request, disbursement_id):
    try:
        disbursement = get_object_or_404(LoanDisbursementTransaction, id=disbursement_id)

        # Update the disbursement fields
        if 'amount' in request.POST:
            disbursement.amount = Decimal(request.POST.get('amount'))
        if 'transaction_date' in request.POST:
            disbursement.transaction_date = datetime.strptime(request.POST.get('transaction_date'), '%Y-%m-%d').date()
        if 'remarks' in request.POST:
            disbursement.remarks = request.POST.get('remarks')

        # Update the updated_by field
        disbursement.updated_by = request.user

        # Save the changes
        disbursement.save()

        return JsonResponse({
            'success': True,
            'disbursement_id': disbursement.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
