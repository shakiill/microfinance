from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.loan.models import Loan, Installment


@receiver(post_save, sender=Loan)
def create_installments(sender, instance, created, **kwargs):
    if created:
        # Calculate monthly installment amount
        monthly_installment = instance.calculate_monthly_installment()
        disbursed_date = instance.disbursed_date

        for month in range(instance.duration_months):
            due_date = disbursed_date + timedelta(days=30 * month)
            Installment.objects.create(
                loan=instance,
                amount=monthly_installment,
                due_date=due_date,
            )
