from django.apps import AppConfig


class LoanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.loan'

    # def ready(self):
    #     import apps.user.signals
