# tables.py
import django_tables2 as tables

from apps.loan.models import LoanApplication, Loan, Installment


class LoanApplicationTable(tables.Table):
    customer_name = tables.Column(
        accessor='customer.name',
        verbose_name='Customer Name',
        attrs={'th': {'class': 'text-left'}}
    )

    customer_mobile = tables.Column(
        accessor='customer.mobile',
        verbose_name='Customer Mobile',
        attrs={'th': {'class': 'text-left'}}
    )

    actions = tables.TemplateColumn(
        template_code='''
            <a href="{% url 'application_details' record.id %}" class="btn btn-sm btn-light-primary"><i class="fa fa-eye"></i></a>
            <a href="{% url 'download_application_details' record.id %}" class="btn btn-sm btn-light-danger"><i class="fa fa-download"></i></a>
        ''',
        orderable=False,
        verbose_name='Actions'
    )

    class Meta:
        model = LoanApplication
        fields = (
            'customer_name', 'customer_mobile', 'amount', 'duration_months', 'status', 'applied_date', 'approved_date')
        attrs = {
            'class': 'table table-hover table-separate table-head-custom table-checkable',
            'id': 'kt_datatable'
        }
        row_attrs = {
            'class': 'text-dark-75'
        }


class LoanTable(tables.Table):
    customer_name = tables.Column(
        accessor='customer.name',
        verbose_name='Customer Name',
        attrs={'th': {'class': 'text-left'}}
    )

    customer_mobile = tables.Column(
        accessor='customer.mobile',
        verbose_name='Customer Mobile',
        attrs={'th': {'class': 'text-left'}}
    )

    actions = tables.TemplateColumn(
        template_code='''
            <a href="{% url 'loan_details' record.id %}" class="btn btn-sm btn-light-danger"><i class="fa fa-eye"></i></a>
        ''',
        orderable=False,
        verbose_name='Actions'
    )

    class Meta:
        model = Loan
        fields = (
        'customer_name', 'customer_mobile', 'principal_amount', 'interest_rate', 'interest', 'duration_months',
        'disbursed_amount', 'status', 'disbursed_date', 'maturity_date')
        attrs = {
            'class': 'table table-hover table-separate table-head-custom table-checkable',
            'id': 'kt_datatable'
        }
        row_attrs = {
            'class': 'text-dark-75'
        }


class RepaymentTable(tables.Table):
    customer_name = tables.Column(
        accessor='loan.customer.name',
        verbose_name='Customer Name',
        attrs={'th': {'class': 'text-left'}}
    )

    customer_mobile = tables.Column(
        accessor='loan.customer.mobile',
        verbose_name='Customer Mobile',
        attrs={'th': {'class': 'text-left'}}
    )

    actions = tables.TemplateColumn(
        template_code='''
                <button type="button" 
                        class="btn btn-sm btn-primary payment-modal-btn" 
                        data-toggle="modal" 
                        data-target="#paymentModal-{{ record.id }}"
                        data-installment-id="{{ record.id }}">
                    View/Pay
                </button>
                {% include "payment_modal.html" %}
            ''',
        orderable=False,
        verbose_name='Actions'
    )

    class Meta:
        model = Installment
        fields = ('customer_name', 'customer_mobile', 'principal_amount', 'interest_amount', 'amount', 'paid_amount','due_date', 'payment_status')
        attrs = {
            'class': 'table table-hover table-separate table-head-custom table-checkable',
            'id': 'kt_datatable'
        }
        row_attrs = {
            'class': 'text-dark-75'
        }
