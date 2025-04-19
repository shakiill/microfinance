# forms.py
from django import forms
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError

from .models import Loan


class LoanGenerationForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['principal_amount', 'interest_rate', 'duration_months', 'disbursed_date', 'interest', 'maturity_date',
                  'assign_by']
        widgets = {
            'disbursed_date': forms.DateInput(attrs={'type': 'date'}),
            'interest': forms.HiddenInput(),
            'maturity_date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the hidden fields not required in the form
        self.fields['interest'].required = False
        self.fields['maturity_date'].required = False
        self.fields['assign_by'].required = True

    def clean(self):
        cleaned_data = super().clean()

        # Get the basic fields
        principal_amount = cleaned_data.get('principal_amount')
        interest_rate = cleaned_data.get('interest_rate')
        duration_months = cleaned_data.get('duration_months')
        disbursed_date = cleaned_data.get('disbursed_date')

        if not all([principal_amount, interest_rate, duration_months, disbursed_date]):
            raise ValidationError("All fields are required")

        try:
            # Calculate total interest
            interest = (principal_amount * (interest_rate / 100) * duration_months) / 12
            cleaned_data['interest'] = round(interest, 2)

            # Calculate maturity date
            maturity_date = disbursed_date + relativedelta(months=duration_months)
            cleaned_data['maturity_date'] = maturity_date

            return cleaned_data
        except Exception as e:
            raise ValidationError(f"Error in calculations: {str(e)}")


from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.http import JsonResponse
from .models import LoanApplication, Installment


@permission_required('loan.add_loan')
@transaction.atomic
def generate_loan(request, application_id):
    if request.method == 'POST':
        try:
            application = LoanApplication.objects.get(id=application_id)

            # Check if loan already exists
            if hasattr(application, 'loan'):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Loan already exists for this application'
                }, status=400)

            form = LoanGenerationForm(request.POST)
            if form.is_valid():
                loan = form.save(commit=False)
                loan.loan_application = application
                loan.save()

                # Generate Installments
                generate_installments(loan)

                return JsonResponse({
                    'status': 'success',
                    'message': 'Loan and Installments generated successfully'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'errors': form.errors
                }, status=400)

        except LoanApplication.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Loan application not found'
            }, status=404)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)


def generate_installments(loan):
    """
    Generate installments for the given loan.
    """
    monthly_interest = loan.interest / loan.duration_months
    monthly_principal = loan.principal_amount / loan.duration_months
    total_monthly_payment = monthly_interest + monthly_principal

    due_date = loan.disbursed_date

    installments = []
    for i in range(loan.duration_months):
        due_date += relativedelta(months=1)  # Increment by 1 month

        installments.append(Installment(
            loan=loan,
            interest_amount=round(monthly_interest, 2),
            principal_amount=round(monthly_principal, 2),
            amount=round(total_monthly_payment, 2),
            due_date=due_date
        ))

    # Bulk create installments
    Installment.objects.bulk_create(installments)
