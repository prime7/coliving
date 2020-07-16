from django import forms
from .models import House,Booking

class DateInput(forms.DateInput):
    input_type = 'date'

class HouseCreateForm(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'title',
            'description',
            'address', 
            'zip_code',
            'city',
            'earliest_move_in',
            'latest_move_out',
            'duration',
            'monthly_rent',
            'has_dishwasher',
            'pets_allowed',
            'heating',
            'has_closet',
            'is_furnished',
            'is_partially_furnished',
            'short_term',
        ]
        widgets = {
            'earliest_move_in': DateInput(attrs={'type': 'date'}),
            'latest_move_out': DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={'placeholder':"Small"}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'start',
            'end',
        ]
        widgets = {
            'start': DateInput(attrs={'type':'date'}),
            'end': DateInput(attrs={'type':'date'})
        }