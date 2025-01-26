from django.core.exceptions import ValidationError
from django.db import models

from apps.helpers.models import TimeStamp
from apps.user.models import Customer, Staff


class Investment(TimeStamp):
    class StatusChoices(models.IntegerChoices):
        APPLIED = 1, 'Applied'
        UNDER_REVIEW = 2, 'Under Review'
        APPROVED = 3, 'Approved'
        ACTIVE = 4, 'Active'
        MATURED = 5, 'Matured'
        REJECTED = 6, 'Rejected'
        WITHDRAWN = 7, 'Withdrawn'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='investments')
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.APPLIED)
    share_certificate_no = models.CharField(max_length=20, unique=True, blank=True, null=True)
    share_certificate_url = models.URLField(blank=True, null=True, help_text="URL to the share certificate")
    number_of_shares = models.PositiveIntegerField(default=1,
                                                   help_text="Number of shares purchased")  # Minimum 1 share required
    share_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      help_text="Price per share in the investment currency")
    investment_date = models.DateField(auto_now_add=True)
    maturity_date = models.DateField(null=True, blank=True,
                                     help_text="The date when the investment matures")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                        help_text="Annual interest rate in percentage (e.g., 5.25)")

    class Meta:
        ordering = ['-investment_date']
        verbose_name = 'Investment'
        verbose_name_plural = 'Investments'

    def __str__(self):
        return f"{self.customer.name} - {self.number_of_shares} shares @ {self.share_price} (Status: {self.get_status_display()})"

    def clean(self):
        # Ensure number of shares is positive
        if self.number_of_shares <= 0:
            raise ValidationError("Number of shares must be greater than zero.")

        # Ensure interest rate is non-negative
        if self.interest_rate < 0:
            raise ValidationError("Interest rate cannot be negative.")

        # Ensure maturity_date is after investment_date
        if self.maturity_date and self.maturity_date < self.investment_date:
            raise ValidationError("Maturity date cannot be earlier than the investment date.")

    def save(self, *args, **kwargs):
        # Trigger validation when saving
        self.full_clean()
        super().save(*args, **kwargs)


class DailySaving(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="savings")
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount saved by the customer")
    date = models.DateField(auto_now_add=True, help_text="Date the saving was made")
    collected_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                                     help_text="Staff member who collected the saving")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of saving creation")
    saving_type = models.CharField(
        max_length=50,
        default='Shonchoy',
        help_text="Type of saving (e.g., Shonchoy for emergency savings)"
    )
    remarks = models.TextField(null=True, blank=True, help_text="Additional remarks for the saving")

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Saving amount must be greater than zero.")

    def __str__(self):
        return f"Saving {self.amount} for {self.customer.name} on {self.date}"


class Withdrawal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount withdrawn from the savings")
    date = models.DateField(auto_now_add=True, help_text="Date of withdrawal")
    collected_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                                     help_text="Staff who processed the withdrawal")
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True, help_text="Remarks about the withdrawal")

    def clean(self):
        # Ensure withdrawal amount does not exceed current savings
        total_savings = self.customer.savings.aggregate(total_savings=models.Sum('amount'))['total_savings'] or 0
        if self.amount > total_savings:
            raise ValidationError("Withdrawal amount exceeds available savings balance.")

    def __str__(self):
        return f"Withdrawal of {self.amount} for {self.customer.name} on {self.date}"
