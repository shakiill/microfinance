from django.db import models

# Create your models here.
class LoanApplication(TimeStamp):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    amount = models.FloatField(default=0)
    months = models.PositiveIntegerField(default=1)


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

    address = models.TextField()
    village = models.CharField(max_length=100, null=True, blank=True)
    post = models.CharField(max_length=100, null=True, blank=True)
    union = models.CharField(max_length=100, null=True, blank=True)
    thana = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    deposit_no = models.CharField(max_length=100, null=True, blank=True)
    deposit_date = models.DateField(null=True, blank=True)
    deposit_amount = models.FloatField(null=True, blank=True)


class CheckInfo(TimeStamp):
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='check_list')
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='check_list')
    # account_type = models.CharField(
    #     max_length=10,
    #     choices=(
    #         ('Savings', 'Savings'),
    #         ('Current', 'Current'),
    #     )
    # )
    account_name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=100)
    check_no = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    remarks = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='check_image', null=True, blank=True)

