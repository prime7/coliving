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
        ]
        widgets = {
            'earliest_move_in': DateInput(attrs={'type': 'date'}),
            'latest_move_out': DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={'placeholder':"Small"}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 100})  
        }
        labels = {
            'is_partially_furnished':"Partially furnished",
        }

class ShortHouseCreateForm(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'title',
            'description',
            'address', 
            'zip_code',
            'city',
            'monthly_rent',
            'has_dishwasher',
            'pets_allowed',
            'heating',
            'has_closet',
            'is_furnished',
            'is_partially_furnished',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':"Small"}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 100})   
        }
        labels = {
            'monthly_rent': 'Rent per day',
            'is_partially_furnished':"Partially furnished",
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