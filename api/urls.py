from rest_framework.routers import DefaultRouter

# Import viewsets
from api.loan.views import (
    LoanApplicationViewSet,
    ApplicationProductViewSet,
    FinancialRecordViewSet,
    CheckInfoViewSet,
    GuarantorViewSet,
    AssetViewSet,
)

router = DefaultRouter()

# Register routes
router.register(r'loan-applications', LoanApplicationViewSet, basename='loan-application')  # Loan application routes
router.register(r'application-products', ApplicationProductViewSet, basename='application-product')  # Product routes
router.register(r'financial-records', FinancialRecordViewSet, basename='financial-record')  # Financial record routes
router.register(r'check-info', CheckInfoViewSet, basename='check-info')  # Check information routes
router.register(r'guarantors', GuarantorViewSet, basename='guarantor')  # Guarantor routes
router.register(r'assets', AssetViewSet, basename='asset')  # Asset routes

urlpatterns = router.urls
