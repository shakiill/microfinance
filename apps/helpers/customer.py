# tables.py
import django_tables2 as tables
import django_filters
from django_filters.widgets import RangeWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div, Fieldset, HTML, Field, Reset
from django import forms
from apps.user.models import Customer


class CustomerTable(tables.Table):
    name = tables.Column(
        # linkify=True,
        verbose_name='Customer',
        attrs={'th': {'class': 'text-left'}}
    )
    actions = tables.TemplateColumn(
        template_code='''
            <a href="{% url 'user_info' record.id %}" class="btn btn-sm btn-light-primary"><i class="fa fa-eye"></i></a>
            <a href="{% url 'user_edit' record.id %}" class="btn btn-sm btn-light-warning"><i class="fa fa-edit"></i></a>
            <a href="{% url 'user_delete' record.id %}" class="btn btn-sm btn-light-danger"><i class="fa fa-trash"></i></a>
        ''',
        orderable=False,
        verbose_name='Actions'
    )

    class Meta:
        model = Customer
        fields = ('name', 'email', 'mobile', 'created_at')
        attrs = {
            'class': 'table table-hover table-separate table-head-custom table-checkable',
            'id': 'kt_datatable'
        }
        row_attrs = {
            'class': 'text-dark-75'
        }


class CustomerFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-2 mb-0'),
                Column('email', css_class='form-group col-md-2 mb-0'),
                Column('mobile', css_class='form-group col-md-2 mb-0'),
                Column('created_at', css_class='form-group col-md-2 mb-0'),
                Column(HTML("""<button class="btn btn-lg btn-primary">Filter</button>"""),
                       css_class='form-group col-md-1 p-5 mb-0'),
            ),
        )


class CustomerFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={
        'class': 'dateinput date-range'}))

    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'created_at']
        form = CustomerFilterForm
