from django.urls import path

from . import views
from .applications import download_application_details
from .loan_process import generate_loan
from ..helpers.views import staff_required

urlpatterns = [
    path('loan/<int:pk>/apply/', staff_required(views.LoanApplicationView.as_view()), name='loan_apply'),
    path('loan/<int:pk>/kyc/', staff_required(views.LoanKYCView.as_view()), name='loan_kyc'),
    path('loan/applications/', staff_required(views.ApplicationListView.as_view()), name='applications'),
    path('application/<int:pk>/download/', download_application_details, name='download_application_details'),
    path('application/<int:pk>/details/', staff_required(views.LoanDetailsView.as_view()), name='application_details'),
    path('application/<int:pk>/change-status/', staff_required(views.LoanStatusChangeView.as_view()), name='application_change_status'),
    path('application/<int:application_id>/generate-loan/', generate_loan, name='generate_loan'),
]
