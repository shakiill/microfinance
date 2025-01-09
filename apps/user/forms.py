from allauth.account.forms import LoginForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordKeyForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from apps.user.models import Customer

User = get_user_model()


# class StaffCreateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'name', 'password1', 'password2')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         for fieldname in self.fields:
#             self.fields[fieldname].help_text = None
#             # self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label
#
#         self.helper = FormHelper()
#         # self.helper.form_show_labels = False
#         self.helper.layout = Layout(
#             Row(
#                 Column('username', css_class='form-group col-md-6 mb-0'),
#                 Column('name', css_class='form-group col-md-6 mb-0'),
#             ),
#             Row(
#                 Column('gender', css_class='form-group col-md-6 mb-0'),
#                 Column('photo', css_class='form-group col-md-6 mb-0'),
#             ),
#             Row(
#                 Column(
#                     Submit('submit', 'Submit'), css_class='kt-login__actions'
#                 )
#             )
#         )


class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=100, label='Name')

    # role = forms.ModelChoiceField(queryset=Group.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                # Column('role', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save'), css_class='kt-login__actions'
                )
            )
        )

    def custom_signup(self, request, user):
        user.name = self.cleaned_data['name']
        # user.groups.add(self.cleaned_data['role'])
        user.save()


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('login', placeholder='Mobile No', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password', placeholder='Password', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    HTML('<label class="checkbox"><input type="checkbox" checked="checked" name="remember">'
                         '<span></span> &nbsp;Remember Me</label>'),
                    css_class='form-group text-left col-md-6 mb-5'),
                Column(
                    HTML('<a href="{}" class="kt-link kt-login__link-forgot">Forgot Password ?</a>'.format(
                        reverse_lazy('account_reset_password'))), css_class='text-right col-md-6 mb-5'
                ),
            ),
            Row(
                Column(
                    Submit('submit', 'Submit'), css_class='kt-login__actions'
                )
            )
        )


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save'), css_class='kt-login__actions mb-5'
                ),
            )
        )


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for fieldname in self.fields:
        # self.fields[fieldname].help_text = None
        # self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('password1', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password2', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save'), css_class='kt-login__actions'
                ),
            )
        )


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = ''

        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('oldpassword', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password2', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save'), css_class='kt-login__actions'
                ),
            )
        )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            # self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label

        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-2'
        # self.helper.field_class = 'col-md-10'
        # self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),

            Row(
                Column(
                    Submit('submit', 'Save')
                ),
            )
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            # self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label

        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Next')
                )
            )
        )


class CustomProfileCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            # self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label

        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    HTML("""<button name="wizard_goto_step" value="0" class="btn btn-primary">Previous</button>"""),
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    Submit('submit', 'Save'),
                    css_class='form-group text-right col-md-6 mb-0'
                )
            )
        )


class NewSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ('username', 'name', 'address', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            # self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label

        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),
                Column('username', css_class='form-group col-md-12 mb-0'),
                Column('email', css_class='form-group col-md-12 mb-0'),
                Column('address', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Register')
                )
            )
        )
