from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Submit
from django import forms

from apps.investment.models import Investment, DailySaving


class InvestmentAddForm(forms.ModelForm):
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1}))

    class Meta:
        model = Investment
        fields = (
            'customer', 'certificate_no', 'number_of_shares', 'share_price', 'interest_rate',
            'investment_date', 'maturity_date', 'remarks')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].required = True

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('customer', css_class='form-group col-md-12 mb-0'),
                Column('certificate_no', css_class='form-group col-md-3 mb-0'),
                Column('number_of_shares', css_class='form-group col-md-3 mb-0'),
                Column('share_price', css_class='form-group col-md-3 mb-0'),
                Column('interest_rate', css_class='form-group col-md-3 mb-0'),
                Column('investment_date', css_class='form-group col-md-3 mb-0'),
                Column('maturity_date', css_class='form-group col-md-3 mb-0'),
                Column('remarks', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save')
                ),
            )
        )


class DailySavingAddForm(forms.ModelForm):
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1}))

    class Meta:
        model = DailySaving
        fields = ('customer', 'date', 'amount', 'remarks')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].required = True

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('customer', css_class='form-group col-md-12 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('amount', css_class='form-group col-md-3 mb-0'),
                Column('remarks', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save')
                ),
            )
        )


class InvestmentFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('customer', css_class='form-group col-md-2 mb-0'),
                Column('status', css_class='form-group col-md-1 mb-0'),
                Column('amount', css_class='form-group col-md-2 mb-0'),
                Column('investment_date', css_class='form-group col-md-3 mb-0'),
                Column('maturity_date', css_class='form-group col-md-3 mb-0'),
                Column(HTML("""<button class="btn btn-lg btn-primary">Filter</button>"""),
                       css_class='form-group col-md-1 p-5 mb-0'),
            ),
        )


class DailySavingFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('customer', css_class='form-group col-md-2 mb-0'),
                Column('collected_by', css_class='form-group col-md-2 mb-0'),
                Column('amount', css_class='form-group col-md-2 mb-0'),
                Column('date', css_class='form-group col-md-2 mb-0'),
                Column('status', css_class='form-group col-md-1 mb-0'),
                Column('created_at', css_class='form-group col-md-2 mb-0'),
                Column(HTML("""<button class="btn btn-lg btn-primary">Filter</button>"""),
                       css_class='form-group col-md-1 p-5 mb-0'),
            ),
        )
