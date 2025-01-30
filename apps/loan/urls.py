from django.urls import path

from . import views
from ..helpers.views import staff_required

urlpatterns = [
    path('loan/<int:pk>/apply/', staff_required(views.LoanApplicationView.as_view()), name='loan_apply'),
    path('loan/<int:pk>/kyc/', staff_required(views.LoanKYCView.as_view()), name='loan_kyc'),
]
