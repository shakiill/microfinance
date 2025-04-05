from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms


class PermissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Define the specific permissions and their custom labels
        self.specific_permissions = {
            "add_customuser": "Create a Staff",  # user.add_customuser
            "change_customuser": "Change a Staff",  # user.change_customuser
            "delete_customuser": "Delete a Staff",  # user.delete_customuser
            "view_customuser": "View a Staff",  # user.view_customuser

            "add_permission": "Add Permissions",  # auth.add_permission

            "add_customer": "Create a Member",  # user.add_customer
            "change_customer": "Change a Member",  # user.change_customer
            "delete_customer": "Delete a Member",  # user.delete_customer
            "view_customer": "View a Member",  # user.view_customer
            "approve_member": "Approve Member",  # user.approve_member

            "add_installment": "Add Installment",  # installment.add_installment
            "change_installment": "Change Installment",  # installment.change_installment
            "delete_installment": "Delete Installment",  # installment.delete_installment
            "view_installment": "View Installment",  # installment.view_installment

            # "add_installmentpay": "Add Installment Payment",  # installment.add_installmentpay
            # "change_installmentpay": "Change Installment Payment",  # installment.change_installmentpay
            # "delete_installmentpay": "Delete Installment Payment",  # installment.delete_installmentpay
            # "view_installmentpay": "View Installment Payment",  # installment.view_installmentpay
            # "payment_approve": "Approve or Decline Payment",  # installment.payment_approve
            # "fine_generate": "Fine Generate",  # installment.fine_generate
            #
            # "add_plot": "Add or Assign Plot",  # project.add_plot
            # "change_plot": "Change Plot",  # project.change_plot
            # "delete_plot": "Delete Plot",  # project.delete_plot
            # "view_plot": "View Plot",  # project.view_plot
            #
            # "add_bulkemail": "Add bulk email",  # dashboard.add_bulkemail
            # "change_bulkemail": "Change bulk email",  # dashboard.change_bulkemail
            # "view_bulkemail": "View bulk email",  # dashboard.view_bulkemail
            # "delete_bulkemail": "Delete bulk email",  # dashboard.delete_bulkemail
            #
            # "member_report": "Member Report",  # user.member_report
            # "installment_report": "Installment Report",  # installment.installment_report
            # "committee_report": "Committee Report",  # cms.committee_report
            # "cms_management": "Content Management",  # cms.cms_management
        }

        # Fetch the specific permissions from the database
        all_permissions = Permission.objects.filter(codename__in=self.specific_permissions.keys())

        # Create checkboxes for each permission
        for perm in all_permissions:
            self.fields[f'perm_{perm.codename}'] = forms.BooleanField(
                label=self.specific_permissions[perm.codename],
                required=False,
                initial=user.has_perm(f'{perm.content_type.app_label}.{perm.codename}')
            )

        # Initialize Crispy Form Helper (if needed)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            # Layout configuration as needed
        )


from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from .models import CustomUser


def manage_permissions(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if not request.user.has_perm('auth.add_permission'):
        return render(request, '403.html')

    if request.method == 'POST':
        form = PermissionForm(request.POST, user=user)
        if form.is_valid():
            all_permissions = Permission.objects.all()
            user.user_permissions.clear()

            for perm in all_permissions:
                perm_field = f'perm_{perm.codename}'  # Use codename to fetch form data
                if form.cleaned_data.get(perm_field):
                    user.user_permissions.add(perm)

            user.save()
            return redirect('staff_list')
    else:
        form = PermissionForm(user=user)

    return render(request, 'manage_permission.html', {'form': form, 'user': user})
