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
        fields = ('username', 'name', 'email', 'password1', 'password2')

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


from django import forms
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import CustomUser


class CustomSignupForm(UserCreationForm):
    name = forms.CharField(max_length=100, label='Full Name', required=True)
    father = forms.CharField(max_length=100, label="Father's Name", required=False)
    mother = forms.CharField(max_length=100, label="Mother's Name", required=False)
    spouse = forms.CharField(max_length=100, label='Spouse Name', required=False)
    education = forms.CharField(max_length=100, label='Education', required=False)
    dob = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(choices=CustomUser.GenderChoices.choices, label='Gender', required=True)
    mobile = forms.CharField(max_length=15, label='Mobile Number', required=True)
    alt_mobile = forms.CharField(max_length=15, label='Alternate Mobile', required=False)

    # Present address
    village = forms.CharField(max_length=50, label='Village', required=False)
    word_no = forms.CharField(max_length=50, label='Word No.', required=False)
    post_office = forms.CharField(max_length=50, label='Post Office', required=False)
    union = forms.CharField(max_length=50, label='Union', required=False)
    upazila = forms.CharField(max_length=50, label='Upazila', required=False)
    district = forms.CharField(max_length=50, label='District', required=False)

    # Permanent address
    is_address = forms.BooleanField(label='Permanent same as present address?', required=False)
    p_village = forms.CharField(max_length=50, label='Permanent Village', required=False)
    p_word_no = forms.CharField(max_length=50, label='Permanent Word No.', required=False)
    p_post_office = forms.CharField(max_length=50, label='Permanent Post Office', required=False)
    p_union = forms.CharField(max_length=50, label='Permanent Union', required=False)
    p_upazila = forms.CharField(max_length=50, label='Permanent Upazila', required=False)
    p_district = forms.CharField(max_length=50, label='Permanent District', required=False)

    class Meta(UserCreationForm):
        model = Customer
        fields = (
            'name', 'email', 'username', 'password1', 'password2', 'dob', 'gender', 'mobile', 'alt_mobile', 'village',
            'word_no', 'post_office', 'union', 'upazila', 'district', 'is_address', 'p_village', 'p_word_no',
            'p_post_office', 'p_union', 'p_upazila', 'p_district', 'father', 'mother', 'spouse', 'education')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label

        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            # Personal Information
            HTML("<h2>Personal Information</h2>"),
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('mobile', css_class='form-group col-md-6'),
            ),
            Row(
                Column('email', css_class='form-group col-md-6'),
                Column('dob', css_class='form-group col-md-6'),
            ),
            Row(
                Column('father', css_class='form-group col-md-6'),
                Column('mother', css_class='form-group col-md-6'),
            ),
            Row(
                Column('spouse', css_class='form-group col-md-6'),
                Column('gender', css_class='form-group col-md-6'),
            ),
            # Present Address
            HTML("<h2>Present Address</h2>"),
            Row(
                Column('village', css_class='form-group col-md-6'),
                Column('word_no', css_class='form-group col-md-6'),
            ),
            Row(
                Column('post_office', css_class='form-group col-md-6'),
                Column('union', css_class='form-group col-md-6'),
            ),
            Row(
                Column('upazila', css_class='form-group col-md-6'),
                Column('district', css_class='form-group col-md-6'),
            ),
            # Permanent Address
            HTML("<h2>Permanent Address</h2>"),
            Row(
                Column('is_address', css_class='form-group col-md-12'),
            ),
            Row(
                Column('p_village', css_class='form-group col-md-6 permanent-address'),
                Column('p_word_no', css_class='form-group col-md-6 permanent-address'),
            ),
            Row(
                Column('p_post_office', css_class='form-group col-md-6 permanent-address'),
                Column('p_union', css_class='form-group col-md-6 permanent-address'),
            ),
            Row(
                Column('p_upazila', css_class='form-group col-md-6 permanent-address'),
                Column('p_district', css_class='form-group col-md-6 permanent-address'),
            ),
            # Password Fields
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
            ),
            # Submit Button
            Row(
                Submit('submit', 'Register', css_class='btn btn-primary btn-block'),
            )
        )

#
# class CustomSignupForm(UserCreationForm):
#
#     class Meta(UserCreationForm):
#         model = Customer
#         fields = ('name', 'email', 'username', 'password1', 'password2')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].label = 'Phone Number'
#
#         for fieldname in self.fields:
#             self.fields[fieldname].help_text = None
#
#         self.helper = FormHelper()
#         # self.helper.form_show_labels = False
#         self.helper.layout = Layout(
#             Row(
#                 Column('name', css_class='form-group col-md-10 mb-0'),
#             ),
#             Row(
#                 Column('username', css_class='form-group col-md-6 mb-0'),
#                 Column('email', css_class='form-group col-md-6 mb-0'),
#             ),
#
#             Row(
#                 Column('password1', css_class='form-group col-md-6 mb-0'),
#                 Column('password2', css_class='form-group col-md-6 mb-0'),
#             ),
#             Row(
#                 Column(
#                     Submit('submit', 'Save')
#                 )
#             )
#         )
