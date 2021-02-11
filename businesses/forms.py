from django import forms
from .models import Store, Product


class StoreForm(forms.ModelForm):

    class Meta:
        model = Store
        fields = (
            'name',
            'description',
        )
        labels = {
            'name': 'Store Name',
            'description': 'Brief Store Description'
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'title',
            'price',
            'description',
            'image'
        )
        labels = {
            'title': 'Product Name',
            'price': 'Product Price',
            'description': 'Brief Description',
        }

