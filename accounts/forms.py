from django import forms
from .validators import validateEmail
from .models import Profile
from django.contrib.auth.password_validation import validate_password


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


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name']