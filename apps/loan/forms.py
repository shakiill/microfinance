from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from apps.loan.models import LoanApplication
from apps.user.models import Customer

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ('customer', 'amount', 'duration_months', 'purpose')

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        user_id = user
        try:
            # Filter the customer queryset
            self.fields['customer'].queryset = Customer.objects.filter(id=user_id)
            self.fields['customer'].required = True

            # Set the default selected customer
            default_customer = Customer.objects.get(id=user_id)
            self.fields['customer'].initial = default_customer

            # Disable the customer field to prevent user changes
            self.fields['customer'].disabled = True
        except Customer.DoesNotExist:
            # Handle the case where the customer does not exist
            self.fields['customer'].queryset = Customer.objects.none()

        # Remove help text for all fields
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None

        # Add form layout using django-crispy-forms
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('customer', css_class='form-group col-md-4 mb-0'),
                Column('amount', css_class='form-group col-md-2 mb-0'),
                Column('duration_months', css_class='form-group col-md-2 mb-0'),
            ),
            Row(
                Column('purpose', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save')
                ),
            )
        )