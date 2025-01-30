from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from apps.helpers.models import TimeStamp
from apps.user.models import Customer


# Create your models here.
class LoanApplication(TimeStamp):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loan_applications')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, help_text="Requested loan amount")
    duration_months = models.PositiveIntegerField(default=1, help_text="Loan duration in months (minimum 1)")
    purpose = models.TextField(null=True, blank=True, help_text="Purpose of the loan")
    status = models.CharField(max_length=50,
                              choices=[
                                  ('PENDING', 'Pending'),
                                  ('APPROVED', 'Approved'),
                                  ('REJECTED', 'Rejected'),
                                  ('DISBURSED', 'Disbursed'),
                                  ('CLOSED', 'Closed'),
                              ],
                              default='PENDING', help_text="Current status of the loan application")
    applied_date = models.DateField(auto_now_add=True)
    approved_date = models.DateField(null=True, blank=True)
    disbursed_date = models.DateField(null=True, blank=True)

    risk_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    credit_committee_approval = models.BooleanField(default=False)
    rejection_reason = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-applied_date']
        verbose_name = 'Loan Application'
        verbose_name_plural = 'Loan Applications'

    def __str__(self):
        return f"Loan #{self.id} - {self.customer.name} - {self.amount}"

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Loan amount must be greater than zero.")
        if self.duration_months < 1:
            raise ValidationError("Loan duration must be at least 1 month.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ApplicationProduct(TimeStamp):
    loan_application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='application_products')
    # product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200, help_text="Name of the product")
    unit_type = models.CharField(max_length=10, help_text="Unite type of the product (e.g., kg, beg,ton, etc.)")
    unit = models.PositiveIntegerField(default=1, help_text="Number of units of the product")
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Price per unit of the product")
    total_price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total price for the product")

    def save(self, *args, **kwargs):
        # Automatically calculate the total price as unit * unit_price
        self.total_price = self.unit * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} - {self.unit} units"


class Guarantor(TimeStamp):
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='guarantors')
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='guarantor')
    name = models.CharField(max_length=100)
    father = models.CharField(max_length=100)
    mother = models.CharField(max_length=100)
    spouse = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    relationship = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='guarantor_photos/', null=True, blank=True)

    address = models.TextField()
    village = models.CharField(max_length=100, null=True, blank=True)
    post = models.CharField(max_length=100, null=True, blank=True)
    union = models.CharField(max_length=100, null=True, blank=True)
    thana = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    deposit_no = models.CharField(max_length=100, null=True, blank=True)
    deposit_date = models.DateField(null=True, blank=True)
    deposit_amount = models.FloatField(null=True, blank=True)


class Asset(TimeStamp):
    class LandTypeChoices(models.TextChoices):
        AGRICULTURAL = 'agricultural', 'Agricultural Land'
        RESIDENTIAL = 'residential', 'Residential Land'
        COMMERCIAL = 'commercial', 'Commercial Land'
        INDUSTRIAL = 'industrial', 'Industrial Land'

    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='lands')
    land_type = models.CharField(max_length=20, choices=LandTypeChoices.choices)
    owner_name = models.CharField(max_length=255)
    mouza_no = models.CharField(max_length=50)
    dag_no = models.CharField(max_length=50)
    khatian_no = models.CharField(max_length=50)
    holding_no = models.CharField(max_length=50)
    land_area = models.DecimalField(max_digits=10, decimal_places=2)  # in decimals
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    year_of_mortgage = models.IntegerField(null=True, blank=True)
    document = models.FileField(upload_to='assets/', null=True, blank=True)


class FinancialRecord(TimeStamp):
    RECORD_TYPE_CHOICES = [
        ('investment', 'Investment'),
        ('loan', 'Existing loan'),
    ]

    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="financial_records")
    loan_application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name="financial_records")
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES, help_text="Type of financial record")

    institution_name = models.CharField(max_length=255, help_text="Name of the financial institution")
    description = models.CharField(max_length=255, null=True, blank=True,
                                   help_text="Description or type of investment/loan (e.g., Fixed Deposit, Mutual Fund, Personal Loan)")
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total amount for the record")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                        help_text="Interest rate of the investment/loan")
    # For investment-specific fields
    maturity_date = models.DateField(null=True, blank=True, help_text="Maturity date for investment (if applicable)")
    # For obligation-specific fields
    outstanding_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                             help_text="Outstanding amount for existing loan (if applicable)")
    monthly_installment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                              help_text="Monthly installment amount (if applicable)")
    end_date = models.DateField(null=True, blank=True, help_text="Expected end date for the obligation (if applicable)")

    def __str__(self):
        return f"{self.institution_name} ({self.record_type})"

    class Meta:
        verbose_name = "Financial Record"
        verbose_name_plural = "Financial Records"


class CheckInfo(TimeStamp):
    application = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='check_list'
    )
    account_name = models.CharField(max_length=100, help_text="Account holder's name")
    account_no = models.CharField(max_length=50, help_text="Account number")
    check_no = models.CharField(max_length=50, help_text="Check number")
    bank_name = models.CharField(max_length=100, help_text="Bank name")
    branch_name = models.CharField(max_length=100, help_text="Branch name")
    remarks = models.TextField(null=True, blank=True, help_text="Additional remarks for the check")
    image = models.ImageField(upload_to='check_images/', null=True, blank=True, help_text="Upload image of the check")

    class Meta:
        verbose_name = 'Check Info'
        verbose_name_plural = 'Check Info Records'

    def __str__(self):
        return f"Check {self.check_no} for Loan #{self.application.id}"


class Loan(TimeStamp):
    application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='loan',
                                       help_text="The approved loan application")
    principal_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Approved loan amount")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate (percentage)")
    duration_months = models.PositiveIntegerField(help_text="Repayment duration in months")
    disbursed_date = models.DateField(null=True, blank=True, help_text="Loan disbursement date")
    maturity_date = models.DateField(null=True, blank=True, help_text="Loan maturity date")
    status = models.CharField(max_length=50,
                              choices=[
                                  ('ACTIVE', 'Active'),
                                  ('CLOSED', 'Closed'),
                                  ('DEFAULTED', 'Defaulted'),
                              ], default='ACTIVE', help_text="Current loan status")
    disbursed_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00,
                                           help_text="disbursed paid so far")

    def calculate_monthly_installment(self):
        """Calculate the fixed monthly installment (EMI)."""
        if self.interest_rate <= 0:
            return self.principal_amount / self.duration_months

        monthly_rate = self.interest_rate / (12 * 100)
        numerator = self.principal_amount * monthly_rate * (1 + monthly_rate) ** self.duration_months
        denominator = (1 + monthly_rate) ** self.duration_months - 1
        return round(numerator / denominator, 2)

    def save(self, *args, **kwargs):
        if not self.disbursed_date:
            self.disbursed_date = now().date()
        if not self.maturity_date:
            self.maturity_date = self.disbursed_date + timedelta(days=30 * self.duration_months)
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return f"Loan #{self.id} - {self.application.customer.name}"


class LoanDisbursementTransaction(TimeStamp):
    class TransactionTypeChoices(models.TextChoices):
        DISBURSEMENT = 'Disbursement', 'Loan Disbursement'

    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name='disbursements',
        help_text="The loan this disbursement belongs to")
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Amount disbursed")
    transaction_date = models.DateField(default=now, help_text="Date of the disbursement transaction")
    transaction_type = models.CharField(max_length=20, choices=TransactionTypeChoices.choices,
                                        default=TransactionTypeChoices.DISBURSEMENT,
                                        help_text="Type of transaction (Disbursement)")
    remarks = models.TextField(null=True, blank=True, help_text="Additional remarks about the disbursement")
    disbursed_to = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loan_disbursements',
                                     help_text="Customer receiving the loan disbursement")

    def save(self, *args, **kwargs):
        # Update loan's disbursed amount (if needed, for auditing purposes)
        if self.pk is None:  # New transaction
            self.loan.disbursed_amount += self.amount
        else:  # Updated transaction
            original = LoanDisbursementTransaction.objects.get(pk=self.pk)
            self.loan.disbursed_amount += self.amount - original.amount

        self.loan.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Loan Disbursement Transaction'
        verbose_name_plural = 'Loan Disbursement Transactions'
        ordering = ['-transaction_date']

    def __str__(self):
        return f"Disbursement of {self.amount} for Loan #{self.loan.id} to {self.disbursed_to.name}"


class Installment(TimeStamp):
    class PaymentStatusChoices(models.TextChoices):
        UNPAID = 'Unpaid', 'Unpaid'
        PARTIAL_PAID = 'Partial Paid', 'Partial Paid'
        PAID = 'Paid', 'Paid'

    class PaymentTimingChoices(models.TextChoices):
        REGULAR = 'Regular', 'Regular'
        LATE = 'Late', 'Late'

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='installments',
                             help_text="The loan this installment belongs to")
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Installment amount")
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text="Amount paid so far")
    due_date = models.DateField(help_text="Date by which this installment should be paid")
    paid_date = models.DateField(null=True, blank=True, help_text="Date when the installment was fully paid")
    payment_status = models.CharField(max_length=15, choices=PaymentStatusChoices.choices,
                                      default=PaymentStatusChoices.UNPAID,
                                      help_text="Payment status of this installment")
    payment_timing = models.CharField(max_length=10, choices=PaymentTimingChoices.choices,
                                      default=PaymentTimingChoices.REGULAR,
                                      help_text="Whether the payment was made on time")
    remarks = models.TextField(null=True, blank=True, help_text="Additional remarks about the installment")

    def save(self, *args, **kwargs):
        # Update payment status based on paid amount
        if self.paid_amount >= self.amount:
            self.payment_status = self.PaymentStatusChoices.PAID
            if not self.paid_date:
                self.paid_date = now().date()
        elif self.paid_amount > 0:
            self.payment_status = self.PaymentStatusChoices.PARTIAL_PAID
        else:
            self.payment_status = self.PaymentStatusChoices.UNPAID

        # Update payment timing based on due date and paid date
        if self.paid_date and self.paid_date > self.due_date:
            self.payment_timing = self.PaymentTimingChoices.LATE
        elif self.paid_date:
            self.payment_timing = self.PaymentTimingChoices.REGULAR

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Installment'
        verbose_name_plural = 'Installments'
        ordering = ['due_date']

    def __str__(self):
        return f"Installment for Loan #{self.loan.id} - Due {self.due_date}"


class Transaction(TimeStamp):
    class TransactionTypeChoices(models.TextChoices):
        PAYMENT = 'Payment', 'Payment'
        ADJUSTMENT = 'Adjustment', 'Adjustment'

    installment = models.ForeignKey(Installment, on_delete=models.CASCADE, related_name='transactions',
                                    help_text="The installment this transaction is linked to")
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Amount of the transaction")
    transaction_date = models.DateField(default=now, help_text="Date of the transaction")
    transaction_type = models.CharField(max_length=20, choices=TransactionTypeChoices.choices,
                                        default=TransactionTypeChoices.PAYMENT,
                                        help_text="Type of transaction (e.g., Payment or Adjustment)")
    remarks = models.TextField(null=True, blank=True, help_text="Additional remarks about the transaction")

    def save(self, *args, **kwargs):
        # Update the linked installment's paid amount whenever a transaction is created/updated
        if self.pk is None:  # New transaction
            self.installment.paid_amount += self.amount
        else:  # Updated transaction
            original = Transaction.objects.get(pk=self.pk)
            self.installment.paid_amount += self.amount - original.amount

        self.installment.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-transaction_date']

    def __str__(self):
        return f"Transaction for Installment #{self.installment.id} - {self.amount}"
