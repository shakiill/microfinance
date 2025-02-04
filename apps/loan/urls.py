from django.urls import path

from . import views
from .applications import download_application_details
from ..helpers.views import staff_required

urlpatterns = [
    path('loan/<int:pk>/apply/', staff_required(views.LoanApplicationView.as_view()), name='loan_apply'),
    path('loan/<int:pk>/kyc/', staff_required(views.LoanKYCView.as_view()), name='loan_kyc'),
    path('application/<int:pk>/download/', download_application_details, name='download_application_details'),
]
