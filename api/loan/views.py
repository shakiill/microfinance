from rest_framework import viewsets
from rest_framework.permissions import BasePermission


class IsStaffAndAuthenticated(BasePermission):
    """
    Custom permission to only allow access to authenticated staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


from api.loan.serializers import LoanApplicationSerializers, GuarantorSerializers, AssetSerializers, \
    ApplicationProductSerializers, FinancialRecordSerializers, CheckInfoSerializers
from apps.helpers.utils import CsrfExemptSessionAuthentication


class LoanApplicationViewSet(viewsets.ModelViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsStaffAndAuthenticated]
    """
    A ViewSet for viewing and editing loan applications.
    This permission class ensures the user is both authenticated and a staff member.
    """
    serializer_class = LoanApplicationSerializers
    queryset = LoanApplicationSerializers.Meta.model.objects.all()


class ApplicationProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsStaffAndAuthenticated]
    """
    A ViewSet for viewing and editing application products.
    """
    serializer_class = ApplicationProductSerializers
    queryset = ApplicationProductSerializers.Meta.model.objects.all()


class FinancialRecordViewSet(viewsets.ModelViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsStaffAndAuthenticated]
    """
    A ViewSet for viewing and editing financial records.
    """
    serializer_class = FinancialRecordSerializers
    queryset = FinancialRecordSerializers.Meta.model.objects.all()


class CheckInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsStaffAndAuthenticated]
    """
    A ViewSet for viewing and editing check information.
    """
    serializer_class = CheckInfoSerializers
    queryset = CheckInfoSerializers.Meta.model.objects.all()


class GuarantorViewSet(viewsets.ModelViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsStaffAndAuthenticated]
    """
    A ViewSet for viewing and editing guarantors.
    """
    serializer_class = GuarantorSerializers
    queryset = GuarantorSerializers.Meta.model.objects.all()


class AssetViewSet(viewsets.ModelViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsStaffAndAuthenticated]
    """
    A ViewSet for viewing and editing assets.
    """
    serializer_class = AssetSerializers
    queryset = AssetSerializers.Meta.model.objects.all()
