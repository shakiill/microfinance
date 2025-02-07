# tables.py
import django_tables2 as tables

from apps.loan.models import LoanApplication


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
            <a href="{% url 'download_application_details' record.id %}" class="btn btn-sm btn-light-warning"><i class="fa fa-edit"></i></a>
            <a href="{% url 'download_application_details' record.id %}" class="btn btn-sm btn-light-danger"><i class="fa fa-download"></i></a>
        ''',
        orderable=False,
        verbose_name='Actions'
    )

    class Meta:
        model = LoanApplication
        fields = ('customer_name', 'customer_mobile', 'amount', 'duration_months', 'status', 'applied_date', 'approved_date')
        attrs = {
            'class': 'table table-hover table-separate table-head-custom table-checkable',
            'id': 'kt_datatable'
        }
        row_attrs = {
            'class': 'text-dark-75'
        }
