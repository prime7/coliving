from django import forms


class CurrentDashForm(forms.Form):

        FRUIT_CHOICES= [
            ('tasker', 'Tasker'),
            ('landlord', 'Landlord'),
            ('tenant', 'Tenant'),
            ]
        dashboard_types = forms.CharField(widget=forms.Select(choices=FRUIT_CHOICES))
