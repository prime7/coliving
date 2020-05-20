from django import forms
from .models import Address,House

class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['lat','lng','address',]

class HouseCreateForm(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'title',
            'description',
            'duration',
            'earliest_move_in',
            'latest_move_out',
            'monthly_rent'
        ]