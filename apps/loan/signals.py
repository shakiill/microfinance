from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.loan.models import Loan, Installment


@receiver(post_save, sender=Loan)
def generate_installments(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            monthly_installment = (instance.principal_amount + instance.interest) / instance.duration_months

            for month in range(instance.duration_months):
                due_date = instance.disbursed_date + relativedelta(months=month + 1)

                Installment.objects.create(
                    loan=instance,
                    amount=round(monthly_installment, 2),
                    due_date=due_date
                )
