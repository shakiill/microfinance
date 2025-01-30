from rest_framework import serializers

from apps.loan.models import LoanApplication, ApplicationProduct, Guarantor, Asset, FinancialRecord, CheckInfo


class LoanApplicationSerializers(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ['id', 'customer', 'amount', 'duration_months', 'purpose']


class ApplicationProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApplicationProduct
        fields = '__all__'


class GuarantorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guarantor
        fields = '__all__'


class AssetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


class FinancialRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = '__all__'


class CheckInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = CheckInfo
        fields = '__all__'
