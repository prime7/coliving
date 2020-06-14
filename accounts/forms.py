from django import forms
from .validators import validateEmail
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from django.utils.safestring import mark_safe
from django import forms



class UserRegisterForm(forms.Form):
    email = forms.EmailField(validators=[validateEmail],label='Email')
    password1 = forms.CharField(validators=[validate_password],widget=forms.PasswordInput(),label='Password')
    password2 = forms.CharField(validators=[validate_password],widget=forms.PasswordInput(),label='Confirm Password')

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError("passwords does not match")


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = mark_safe(f'<br><img src="{value.url}" class="img-fluid" width="120" height="120"/>')
        return f'{input_html}{img_html}'



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','profile_pic','mobile_number','bio',]
        widgets = {
            'profile_pic': ImagePreviewWidget(),
        }

class ProfileConnectForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','mobile_number','bio']