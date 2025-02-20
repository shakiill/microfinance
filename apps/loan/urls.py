from django.urls import path

from . import views
from .applications import download_application_details
from .loan_process import generate_loan
from .transections import create_disbursement, update_disbursement, make_payment
from ..helpers.views import staff_required

urlpatterns = [
    path('loan/<int:pk>/apply/', staff_required(views.LoanApplicationView.as_view()), name='loan_apply'),
    path('loan/<int:pk>/kyc/', staff_required(views.LoanKYCView.as_view()), name='loan_kyc'),

    path('loan/applications/', staff_required(views.ApplicationListView.as_view()), name='applications'),
    path('all/', staff_required(views.LoanListView.as_view()), name='all_loans'),

    path('<int:pk>/details/', staff_required(views.LoanDetailsView.as_view()), name='loan_details'),
    path('<int:loan_id>/create-disbursement/', create_disbursement, name='create_disbursement'),
    path('<int:disbursement_id>/update-disbursement/', update_disbursement, name='update_disbursement'),
    path('installments/<int:installment_id>/details/', views.installment_details, name='installment_details'),
    path('installment/<int:installment_id>/payment/', make_payment, name='make_payment'),

    path('application/<int:pk>/download/', download_application_details, name='download_application_details'),
    path('application/<int:pk>/details/', staff_required(views.LoanApplicationDetailsView.as_view()),
         name='application_details'),
    path('application/<int:pk>/change-status/', staff_required(views.LoanStatusChangeView.as_view()),
         name='application_change_status'),
    path('application/<int:application_id>/generate-loan/', generate_loan, name='generate_loan'),

    path('repayments/', staff_required(views.RepaymentListView.as_view()), name='repayments'),
    path('transactions/<int:installment_id>/', views.get_transaction_history, name='transaction_history'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),

    path('all_transactions/', staff_required(views.AllTransectionListView.as_view()), name='all_transactions'),
]
