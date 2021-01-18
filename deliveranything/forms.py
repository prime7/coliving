from django import forms
from django.core.validators import MinValueValidator

from .models import Business, Address, Delivery, AnonymousDelivery, Vehicle, year_choices, current_year

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
    year = forms.IntegerField(min_value=1984, max_value=current_year())

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


class AnonymousDeliveryForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.DateInput(
        attrs={
            'type': 'date'
        }),
        required=True,
    )
    date_time = forms.TimeField(widget=forms.TimeInput(
        attrs={
            'type': 'time'
        }),
        label='Time',
        required=True,
        help_text='Hr-Min-AM/PM'
    )

    class Meta:
        model = AnonymousDelivery
        fields = (
            'user',
            'pickup',
            'dropoff',
            'date',
            'date_time',
            'description',
            'weight',
            'length',
            'width',
            'height',
            'wait_time'
        )
        labels = {
            'user': "Email",
            'date_time': "Time",
            'wait_time': "Expected Wait Time"
        }



class DeliveryForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.DateInput(
        attrs={
            'type': 'date'
        }),
        required=True,
    )
    date_time = forms.TimeField(widget=forms.TimeInput(
        attrs={
            'type': 'time'
            }),
        label='Time',
        required=True,
        help_text='Hr-Min-AM/PM'
    )

    class Meta:
        model = Delivery
        fields = (
            'pickup',
            'dropoff',
            'date',
            'date_time',
            'description',
            'weight',
            'length',
            'width',
            'height',
            'wait_time'
        )
        labels = {
            'date_time': "Time",
            'wait_time': "Expected Wait Time"
        }

