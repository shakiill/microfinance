# tables.py
import django_tables2 as tables

from apps.loan.models import LoanApplication, Loan, Installment, Transaction, LoanDisbursementTransaction


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

    paid_amount = tables.Column(
        attrs={
            'td': {'class': 'paid-amount-cell'},
            'th': {'class': 'text-left'}
        }
    )

    payment_status = tables.Column(
        attrs={
            'td': {'class': 'payment-status-cell'},
            'th': {'class': 'text-left'}
        }
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
        fields = (
        'customer_name', 'customer_mobile', 'principal_amount', 'interest_amount', 'amount', 'paid_amount',
        'due_date', 'payment_status')
        attrs = {
            'class': 'table table-hover table-separate table-head-custom table-checkable',
            'id': 'kt_datatable'
        }
        row_attrs = {
            'class': 'text-dark-75'
        }


class TransactionTable(tables.Table):
    customer_name = tables.Column(
        accessor='installment.loan.customer.name',
        verbose_name='Customer Name',
        attrs={'th': {'class': 'text-left'}}
    )

    customer_mobile = tables.Column(
        accessor='installment.loan.customer.mobile',
        verbose_name='Customer Mobile',
        attrs={'th': {'class': 'text-left'}}
    )

    collected_by = tables.Column(
        accessor='collected_by.name',
        verbose_name='Collected by',
        attrs={'th': {'class': 'text-left'}}
    )

    actions = tables.TemplateColumn(
        template_code='''
                   <button class="btn btn-sm btn-primary change-status" 
                           data-id="{{ record.id }}"
                           data-status="{{ record.status }}"
                           data-toggle="modal"
                           data-target="#statusModal">
                       Status
                   </button>
                   <button class="btn btn-sm btn-danger delete-record" 
                    data-id="{{ record.id }}"
                    data-name="{{ record.name|default:record.id }}">
                Delete
            </button>
               ''',
        orderable=False,
        verbose_name='Actions'
    )

    class Meta:
        model = Transaction
        fields = (
            'customer_name', 'customer_mobile', 'amount', 'transaction_date',
            'amount', 'collected_by', 'status', 'verified_at', 'verified_by')
        attrs = {
            'class': 'table table-hover table-separate table-head-custom table-checkable',
            'id': 'kt_datatable'
        }
        row_attrs = {
            'class': 'text-dark-75'
        }


class LoanDisbursementTransactionTable(tables.Table):
    customer_name = tables.Column(
        accessor='disbursed_to.name',
        verbose_name='Customer Name',
        attrs={'th': {'class': 'text-left'}}
    )

    customer_mobile = tables.Column(
        accessor='disbursed_to.mobile',
        verbose_name='Customer Mobile',
        attrs={'th': {'class': 'text-left'}}
    )
    loan_id = tables.Column(
        accessor='loan.loan_application.id',
        verbose_name='Loan ID',
        attrs={'th': {'class': 'text-left'}}
    )


    class Meta:
        model = LoanDisbursementTransaction
        fields = ('transaction_date', 'loan_id',  'amount', 'customer_name', 'customer_mobile')
        attrs = {
            'class': 'table table-hover table-separate table-head-custom table-checkable',
            'id': 'kt_datatable'
        }
        row_attrs = {
            'class': 'text-dark-75'
        }
