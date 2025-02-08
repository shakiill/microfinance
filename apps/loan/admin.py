from django.contrib import admin

from apps.loan.models import Installment, Loan


# Register your models here.
@admin.register(Loan)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['loan_application', 'principal_amount', 'interest_rate', 'duration_months', 'disbursed_date', 'interest',
                    'maturity_date', 'status']


@admin.register(Installment)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'paid_amount', 'payment_status']
