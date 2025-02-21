import django_tables2 as tables

from apps.investment.models import Investment


class InvestmentTable(tables.Table):
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
            <div class="d-flex gap-2">
                <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#editModal-{{ record.id }}">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button type="button" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal-{{ record.id }}">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </div>

            <!-- Edit Modal -->
            <div class="modal fade" id="editModal-{{ record.id }}" tabindex="-1" aria-labelledby="editModalLabel-{{ record.id }}" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="editModalLabel-{{ record.id }}">Edit Investment</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form method="POST" action="{% url 'investment-update' record.id %}" class="edit-investment-form">
                            <div class="modal-body">
                                {% csrf_token %}
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label for="number_of_shares-{{ record.id }}" class="form-label">Number of Shares</label>
                                        <input type="number" class="form-control" id="number_of_shares-{{ record.id }}" 
                                               name="number_of_shares" value="{{ record.number_of_shares }}">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label for="share_price-{{ record.id }}" class="form-label">Share Price</label>
                                        <input type="number" step="0.01" class="form-control" id="share_price-{{ record.id }}" 
                                               name="share_price" value="{{ record.share_price }}">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label for="interest_rate-{{ record.id }}" class="form-label">Interest Rate (%)</label>
                                        <input type="number" step="0.01" class="form-control" id="interest_rate-{{ record.id }}" 
                                               name="interest_rate" value="{{ record.interest_rate }}">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label for="maturity_date-{{ record.id }}" class="form-label">Maturity Date</label>
                                        <input type="date" class="form-control" id="maturity_date-{{ record.id }}" 
                                               name="maturity_date" value="{{ record.maturity_date|date:'Y-m-d' }}">
                                    </div>
                                    <div class="col-12 mb-3">
                                        <label for="remarks-{{ record.id }}" class="form-label">Remarks</label>
                                        <textarea class="form-control" id="remarks-{{ record.id }}" 
                                                  name="remarks" rows="3">{{ record.remarks }}</textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="submit" class="btn btn-primary">Save changes</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Delete Modal -->
            <div class="modal fade" id="deleteModal-{{ record.id }}" tabindex="-1" aria-labelledby="deleteModalLabel-{{ record.id }}" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="deleteModalLabel-{{ record.id }}">Confirm Delete</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            Are you sure you want to delete this investment?<br>
                            <strong>Certificate No:</strong> {{ record.certificate_no }}<br>
                            <strong>Shares:</strong> {{ record.number_of_shares }} @ {{ record.share_price }}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <form method="POST" action="{% url 'investment-delete' record.id %}" style="display: inline;">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-danger">Delete</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            ''',
        orderable=False,
        verbose_name='Actions'
    )

    class Meta:
        model = Investment
        fields = (
            'certificate_no', 'customer_name', 'customer_mobile',
            'number_of_shares', 'share_price', 'interest_rate', 'investment_date', 'maturity_date', 'status')
        attrs = {
            'class': 'table table-hover table-separate table-head-custom table-checkable',
            'id': 'kt_datatable'
        }
        row_attrs = {
            'class': 'text-dark-75'
        }
