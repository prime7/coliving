from django import forms
from .models import Agreement
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = 'date'

class AgreementCreateForm(forms.ModelForm):
    def clean_tenants_email(self):
        email = self.cleaned_data['tenants_email']
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError("Tenant email was not found in our database")

        return email
    def __init__(self, *args, **kwargs):
        super(AgreementCreateForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('property_type', css_class='form-group col-md-6 mb-0'),
                Column('lease_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('lease_start_date', css_class='form-group col-md-6 mb-0'),
                Column('lease_end_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('location', css_class='form-group col-md-6 mb-0'),
                Column('landlord_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('landlord_phone', css_class='form-group col-md-6 mb-0'),
                Column('tenant_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('tenant_phone_number', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('other_occupants_allowed', css_class='form-group col-md-6 mb-0'),
                Column('parking_access', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('smoking_allowed', css_class='form-group col-md-4 mb-0'),
                Column('vaping_allowed', css_class='form-group col-md-4 mb-0'),
                Column('pets_allowed', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('monthly_rent', css_class='form-group col-md-4 mb-0'),
                Column('security_deposit', css_class='form-group col-md-4 mb-0'),
                Column('utility_cost', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('maintenance_cost', css_class='form-group col-md-6 mb-0'),
                Column('improvements', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('sublease', css_class='form-group col-md-6 mb-0'),
                Column('renew', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('tenants_email', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Create Agreement')
        )
    class Meta:
        model = Agreement
        fields = [
            'property_type',
            'lease_type',
            'lease_start_date',
            'lease_end_date',
            'location',
            'landlord_type',
            'landlord_phone',
            'tenant_name',
            'other_occupants_allowed',
            'tenant_phone_number',
            'parking_access',
            'smoking_allowed',
            'vaping_allowed',
            'pets_allowed',
            'monthly_rent',
            'security_deposit',
            'utility_cost',
            'maintenance_cost',
            'improvements',
            'sublease',
            'renew',
            'tenants_email',
        ]
        widgets = {
            'lease_start_date': DateInput(),
            'lease_end_date': DateInput(),
            'location': forms.widgets.TextInput(attrs={'placeholder':"EG. Street Apt No"}),
            'landlord_phone': forms.widgets.TextInput(attrs={'placeholder':"Landlords phone number"}),
            'tenant_name': forms.widgets.TextInput(attrs={'placeholder':"Tenants name"}),
            'tenant_phone_number': forms.widgets.TextInput(attrs={'placeholder':"Tenants phone number"}),
            'tenants_email': forms.widgets.TextInput(attrs={'placeholder':"This is very important to make the contract"}),
        }
        labels = {
            'property_type':"What type of property is being rented?",
            'lease_type':"What type of lease term do you want?",
            'lease_start_date':"When is the lease starting?",
            'lease_end_date':"When is the lease ending?",
            'location':"Where it is located?",
            'landlord_type':"Who is the landlord?",
            'landlord_phone':"How can the landlord be connected?",
            'tenant_name':"Who will be paying rent?",
            'other_occupants_allowed':"Will there any extra occupants can live in the property?",
            'tenant_phone_number':"How can the tenant be connected?",
            'parking_access':"Will the tenant have access to parking?",
            'smoking_allowed':"Is smoking allowed indoors?",
            'vaping_allowed':"Is vaping allowed indoors?",
            'pets_allowed':"Is pets allowed?",
            'monthly_rent':"What is the monthly rent?",
            'security_deposit':"How much do you want as security deposit?",
            'utility_cost':"Who is responsible for paying utility cost?",
            'maintenance_cost':"Will the tenant be responsible for any maintenance?",
            'improvements':"Will the tenant be allowed to make any improvements to the property?",
            'sublease':"Can the tenant assign/sublease the property?",
            'renew':"Will the tenant have option to renew the lease?",
        }

