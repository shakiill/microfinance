# forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div, HTML, Field
from django import forms

from .models import Customer, ProfessionInfo, AdditionalBusiness


class CustomerBasicForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'father', 'mother', 'spouse', 'education',
                  'dob', 'gender', 'mobile', 'alt_mobile', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'basic-form'
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column('name', css_class='form-group col-md-12 mb-0'),
                        Column('father', css_class='form-group col-md-12 mb-0'),
                        Column('mother', css_class='form-group col-md-12 mb-0'),
                        Column('spouse', css_class='form-group col-md-12 mb-0'),
                        Column('education', css_class='form-group col-md-12 mb-0'),

                    )
                    , css_class='form-group col-md-4 mb-0'),
                Column(
                    Row(
                        Column('dob', css_class='form-group col-md-12 mb-0'),
                        Column('gender', css_class='form-group col-md-12 mb-0'),
                        Column('mobile', css_class='form-group col-md-12 mb-0'),
                        Column('alt_mobile', css_class='form-group col-md-12 mb-0'),
                    )
                    , css_class='form-group col-md-4 mb-0'),

                Column(
                    Row(
                        Column(HTML('<h4>Photo</h4>'), css_class='form-group col-md-12 mb-0'),
                        Column(
                            Field('photo', template='layout/fields/image_thumbnail.html')
                            , css_class='form-group col-md-12'
                        ),
                    )
                    , css_class='form-group col-md-4 mb-0'),

            ),
            Div(
                HTML('<input type="hidden" name="step" value="basic">')
            ),
            Row(
                Column(
                    Submit('submit', 'Save Basic Information', css_class='btn btn-primary'),
                    css_class='text-center'
                ), css_class='form-group col-md-12 mb-0'),

        )


class AddressForm(forms.ModelForm):
    # Present address
    village = forms.CharField(max_length=50, label='Village', required=False)
    word_no = forms.CharField(max_length=50, label='Word No.', required=False)
    post_office = forms.CharField(max_length=50, label='Post Office', required=False)
    union = forms.CharField(max_length=50, label='Union', required=False)
    upazila = forms.CharField(max_length=50, label='Upazila', required=False)
    district = forms.CharField(max_length=50, label='District', required=False)

    # Permanent address
    is_address = forms.BooleanField(label='Permanent same as present address?', required=False)
    p_village = forms.CharField(max_length=50, label='Village', required=False)
    p_word_no = forms.CharField(max_length=50, label='Word No.', required=False)
    p_post_office = forms.CharField(max_length=50, label='Post Office', required=False)
    p_union = forms.CharField(max_length=50, label='Union', required=False)
    p_upazila = forms.CharField(max_length=50, label='Upazila', required=False)
    p_district = forms.CharField(max_length=50, label='District', required=False)

    class Meta:
        model = Customer
        fields = ['village', 'word_no', 'post_office', 'union', 'upazila', 'district',
                  'is_address', 'p_village', 'p_word_no', 'p_post_office', 'p_union',
                  'p_upazila', 'p_district']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'address-form'
        self.helper.layout = Layout(

            Row(
                Column(
                    Row(
                        HTML("<h5>Present Address:</h5>"),
                        Column('village', css_class='form-group col-md-10 mb-0'),
                        Column('word_no', css_class='form-group col-md-10 mb-0'),
                        Column('post_office', css_class='form-group col-md-10 mb-0'),
                        Column('union', css_class='form-group col-md-10 mb-0'),
                        Column('upazila', css_class='form-group col-md-10 mb-0'),
                        Column('district', css_class='form-group col-md-10 mb-0'),
                    )
                    , css_class='form-group col-md-6 mb-0'),
                Column(
                    Row(
                        HTML("<h5>Permanent Address</h5>"),
                        Column('is_address', css_class='form-group col-md-10 mb-0'),
                        Column('p_village', css_class='form-group col-md-10 permanent-address mb-0'),
                        Column('p_word_no', css_class='form-group col-md-10 permanent-address mb-0'),
                        Column('p_post_office', css_class='form-group col-md-10 permanent-address mb-0'),
                        Column('p_union', css_class='form-group col-md-10 permanent-address mb-0'),
                        Column('p_upazila', css_class='form-group col-md-10 permanent-address mb-0'),
                        Column('p_district', css_class='form-group col-md-10 permanent-address mb-0'),
                    )
                    , css_class='form-group col-md-6 mb-0'),
            ),

            Div(
                HTML('<input type="hidden" name="step" value="address">'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save Address Information', css_class='btn btn-primary'),
                    css_class='text-center'
                ), css_class='form-group col-md-12 mb-0'),
        )


class ProfessionInfoForm(forms.ModelForm):
    class Meta:
        model = ProfessionInfo
        exclude = ['customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'profession-form'
        self.helper.layout = Layout(
            Row(
                Column('business_owner', css_class='form-group col-md-6'),
                Column('job_holder', css_class='form-group col-md-6'),
            ),
            Row(
                Column('agriculture_land_area', css_class='form-group col-md-6'),
                Column('home_land_area', css_class='form-group col-md-6'),
            ),
            Row(
                Column('vehicle', css_class='form-group col-md-6'),
                Column('tin', css_class='form-group col-md-6'),
            ),
            'nid',
            # Business Info
            Row(
                Column('trade_license', css_class='form-group col-md-6'),
                Column('business_type', css_class='form-group col-md-6'),
            ),
            'business_address',
            Row(
                Column('business_start', css_class='form-group col-md-6'),
                Column('business_capital', css_class='form-group col-md-6'),
            ),
            Row(
                Column('sales_amount', css_class='form-group col-md-4'),
                Column('dps', css_class='form-group col-md-4'),
                Column('fdr', css_class='form-group col-md-4'),
            ),
            # Job Info
            Row(
                Column('job_title', css_class='form-group col-md-6'),
                Column('industry', css_class='form-group col-md-6'),
            ),
            Row(
                Column('job_start', css_class='form-group col-md-6'),
                Column('salary', css_class='form-group col-md-6'),
            ),
            'job_location',
            Div(
                Submit('submit', 'Save Profession Information', css_class='btn btn-primary'),
                css_class='text-right'
            ),
            Div(
                HTML('<input type="hidden" name="step" value="profession">'),
            )
        )


class AdditionalBusinessForm(forms.ModelForm):
    class Meta:
        model = AdditionalBusiness
        exclude = ['customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('type', css_class='form-group col-md-6'),
            ),
            'address',
            Row(
                Column('trade_license', css_class='form-group col-md-6'),
                Column('start', css_class='form-group col-md-6'),
            ),
            Row(
                Column('capital', css_class='form-group col-md-12'),
            ),
        )


# forms.py
AdditionalBusinessFormSet = forms.inlineformset_factory(
    Customer,
    AdditionalBusiness,
    form=AdditionalBusinessForm,
    extra=0,  # Changed from 1 to 0 to not show extra form by default
    can_delete=True
)
# views.py

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer, ProfessionInfo


def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    profession_info, created = ProfessionInfo.objects.get_or_create(customer=customer)

    # Get the current step from either POST or GET
    current_step = request.POST.get('step') or request.GET.get('step', 'basic')

    # Initialize all forms
    basic_form = CustomerBasicForm(instance=customer)
    address_form = AddressForm(instance=customer)
    profession_form = ProfessionInfoForm(instance=profession_info)
    business_formset = AdditionalBusinessFormSet(instance=customer)

    if request.method == 'POST':
        if current_step == 'basic':
            basic_form = CustomerBasicForm(request.POST, request.FILES, instance=customer)
            if basic_form.is_valid():
                basic_form.save()
                messages.success(request, 'Basic information updated successfully.')
                return redirect(f'{request.path}?step=basic')

        elif current_step == 'address':
            address_form = AddressForm(request.POST, instance=customer)
            if address_form.is_valid():
                address_form.save()
                messages.success(request, 'Address information updated successfully.')
                return redirect(f'{request.path}?step=address')

        elif current_step == 'profession':
            profession_form = ProfessionInfoForm(request.POST, instance=profession_info)
            if profession_form.is_valid():
                profession_form.save()
                messages.success(request, 'Profession information updated successfully.')
                return redirect(f'{request.path}?step=profession')

        elif current_step == 'business':
            business_formset = AdditionalBusinessFormSet(
                request.POST,
                instance=customer,
                prefix='business'  # Add prefix to avoid form conflicts
            )
            if business_formset.is_valid():
                instances = business_formset.save(commit=False)
                # Handle deleted forms
                for obj in business_formset.deleted_objects:
                    obj.delete()
                # Save new and modified instances
                for instance in instances:
                    instance.customer = customer
                    instance.save()
                business_formset.save_m2m()
                messages.success(request, 'Additional business information updated successfully.')
                return redirect(f'{request.path}?step=business')
            else:
                print(business_formset.errors)  # For debugging
    else:
        # Initialize formset with prefix for GET requests
        business_formset = AdditionalBusinessFormSet(
            instance=customer,
            prefix='business'
        )

    context = {
        'customer': customer,
        'basic_form': basic_form,
        'address_form': address_form,
        'profession_form': profession_form,
        'business_formset': business_formset,
        'active_step': current_step
    }

    return render(request, 'customer_edit.html', context)
