from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import DefaultStorage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, FormView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from formtools.wizard.views import SessionWizardView

from .forms import (ProfileUpdateForm,
                    CustomProfileCreateForm, CustomSignupForm, NewSignUpForm, CustomUserEditForm
                    )
from .models import Customer
from ..helpers.customer import CustomerTable, CustomerFilterSet
from ..helpers.views import PageHeaderMixin
from ..loan.models import LoanApplication

# Create your views here.

User = get_user_model()


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    # permission_required = 'user.change_user'
    model = User
    form_class = ProfileUpdateForm
    template_name = 'account/add.html'
    success_url = reverse_lazy('home')
    success_message = "Profile was updated successfully"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


# class ProfileDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
class ProfileDetailView(LoginRequiredMixin, DetailView):
    # permission_required = 'user.view_user'
    model = User
    template_name = 'account/detail.html'

    def get_object(self, queryset=None):
        return self.request.user


class RegistrationWizardView(SessionWizardView):
    file_storage = DefaultStorage()
    template_name = "account/registration.html"
    form_list = [CustomSignupForm, CustomProfileCreateForm]
    instance = None

    def get_form_instance(self, step):
        if self.instance is None:
            self.instance = User()
        return self.instance

    def done(self, form_list, **kwargs):
        self.instance.save()
        return redirect(reverse_lazy('account_login'))


class UserListView(PageHeaderMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'configuration.view_customuser'
    model = Customer
    template_name = 'list.html'
    paginate_by = 10
    ordering = '-id'
    table_class = CustomerTable
    filterset_class = CustomerFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Customers',
            'add_link': reverse_lazy('user_add'),
            'filter': self.filterset
        })
        return context


class UserCreateView(LoginRequiredMixin, PageHeaderMixin, FormView):
    permission_required = 'user.add_customer'
    model = Customer
    form_class = CustomSignupForm
    success_url = reverse_lazy('user_list')
    template_name = 'add.html'

    def form_valid(self, form):
        user = form.save(self.request)  # Ensures `custom_signup` is called

        # if form.cleaned_data['is_address']:
        #     user.p_village = form.cleaned_data['village']
        #     user.p_word_no = form.cleaned_data['word_no']
        #     user.p_post_office = form.cleaned_data['post_office']
        #     user.p_union = form.cleaned_data['union']
        #     user.p_upazila = form.cleaned_data['upazila']
        #     user.p_district = form.cleaned_data['district']

        user.save()
        return super().form_valid(form)


class UserEditView(LoginRequiredMixin, PageHeaderMixin, UpdateView):
    permission_required = 'user.change_customer'
    model = Customer
    form_class = CustomUserEditForm
    template_name = 'add.html'
    success_url = reverse_lazy('user_list')


class UserInfoView(LoginRequiredMixin, PageHeaderMixin, DetailView):
    permission_required = 'user.view_customer'
    model = Customer
    template_name = 'user/info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = LoanApplication.objects.filter(customer=self.object)
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user_list')
    template_name = 'delete.html'


def signup(request):
    if request.method == 'POST':
        form = NewSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL
    else:
        form = NewSignUpForm()
    return render(request, 'account/signup.html', {'form': form})
