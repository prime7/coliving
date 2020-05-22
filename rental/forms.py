from django import forms
from .models import House


class DateInput(forms.DateInput):
    input_type = 'date'

class HouseCreateForm(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'title',
            'description',
            'duration',
            'earliest_move_in',
            'latest_move_out',
            'monthly_rent',
            'lat',
            'lng',
            'address'
        ]
        widgets = {
            'earliest_move_in': DateInput(attrs={'type': 'date'}),
        }