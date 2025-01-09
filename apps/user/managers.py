from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.db import models


class StaffManager(BaseUserManager):
    def get_queryset(self):
        return super(StaffManager, self).get_queryset().filter(is_staff=True, is_superuser=False)


class CustomerManager(BaseUserManager):
    def get_queryset(self):
        return super(CustomerManager, self).get_queryset().filter(groups__name='customer')
