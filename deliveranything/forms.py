from django import forms
from .models import Business, Address, Delivery, DeliveryImage, Vehicle

class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = (
            'street_address',
            'apartment_address',
            'business_city',
            'business_country',
            'postal_code',
        )
        labels = {
            'street_address': 'Address Line 1',
            'apartment_address': 'Address Line 2',
            'business_city': 'Business City',
            'business_country': 'Business Country',
            'postal_code': 'Postal Code',
        }

class BusinessCreationForm(forms.ModelForm):

    class Meta:
        model = Business
        fields = (
            'business_name',
            'verification_doc',
        )
        labels = {
            'business_name': "Business Name",
        }


class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = (
            'drivers_licence_number',
            'registration',
            'make',
            'model',
            'year',
            'color',
        )
        labels = {
            'drivers_licence_number': 'Drivers Licence Number',
            'registration': 'Registration Number'
        }


class DeliveryForm(forms.ModelForm):

    class Meta:
        model = Delivery
        fields = (
            'pickup',
            'dropoff',
            'time',
            'description',
            'length',
            'width',
            'height'
        )
        labels = {
            'time': "Date"
        }
        widgets = {
            'time': DateTimeInput()
        }

