from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django import forms


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
