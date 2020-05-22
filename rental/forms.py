from django import forms
from .models import House,Image
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.helper import FormHelper

class DateInput(forms.DateInput):
    input_type = 'date'

class HouseCreateForm(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'title',
            'description',
            'earliest_move_in',
            'latest_move_out',
            'duration',
            'monthly_rent',
            'lat',
            'lng',
            'address',
        ]
        widgets = {
            'earliest_move_in': DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={'placeholder':"Title"})
        }
    def __init__(self, *args, **kwargs):
        super(HouseCreateForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            Row(
                Column('earliest_move_in', css_class='form-group col-md-6 mb-0'),
                Column('latest_move_out', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('duration', css_class='form-group col-md-6 mb-0'),
                Column('monthly_rent', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('lat', css_class='form-group col-md-6 mb-0'),
                Column('lng', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'address',
        )
