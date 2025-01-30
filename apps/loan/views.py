from django.urls import reverse
from django.views.generic import CreateView, DetailView

from apps.loan.forms import LoanApplicationForm
from apps.loan.models import LoanApplication, ApplicationProduct, Guarantor, Asset, FinancialRecord, CheckInfo


# Create your views here.
class LoanApplicationView(CreateView):
    model = LoanApplication
    form_class = LoanApplicationForm
    template_name = 'loan_add.html'

    def get_success_url(self):
        return reverse('loan_kyc', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super(LoanApplicationView, self).get_form_kwargs()
        pk = self.kwargs.get('pk')  # Get the user ID from the URL
        kwargs.update({'user': pk})  # Pass the user ID as a keyword argument
        return kwargs

class LoanKYCView(DetailView):
    model = LoanApplication
    template_name = 'kyc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ApplicationProduct.objects.filter(loan_application=self.object)
        context['guarantors'] = Guarantor.objects.filter(application=self.object)
        context['assets'] = Asset.objects.filter(application=self.object)
        context['financials'] = FinancialRecord.objects.filter(loan_application=self.object)
        context['checks'] = CheckInfo.objects.filter(application=self.object)
        return context
