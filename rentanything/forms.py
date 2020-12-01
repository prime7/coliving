from django import forms
from .models import Booking, Listing

class DateInput(forms.DateInput):
    input_type = 'date'

class ListingCreateForm(forms.ModelForm):
    class Meta:
        model = Listing

        fields = [
            'title',
            'category',
            'price',
            'payment_interval',
            'fragile',
            'packaging',
            'condition',
            'country',
            'area',
            'city',
            'amount',
            'booking_limit',
            'description',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':"Title"}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 100})
        }
        labels = {
            'payment_interval': 'Payment Interval',
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
