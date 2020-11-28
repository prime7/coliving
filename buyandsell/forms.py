from django import forms
from .models import Posting, Offer

class DateInput(forms.DateInput):
    input_type = 'date'

class PostingCreateForm(forms.ModelForm):
    class Meta:
        model = Posting

        fields = [
            'title',
            'category',
            'price',
            'condition',
            'country',
            'area',
            'city',
            'amount',
            'description',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':"Title"}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 100})
        }

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'offering_price',
        ]

