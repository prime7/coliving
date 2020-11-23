from .models import Profile,Contact
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = mark_safe(f'<br><img src="{value.url}" class="img-fluid" width="120" height="120"/>')
        return f'{input_html}{img_html}'

class ProfileVerificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['verification_doc']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','bio',]
        widgets = {
            'profile_pic': ImagePreviewWidget(),
        }

class ProfileConnectForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email','reason','subject','description',]
        labels = {
            'email':'Your email address',
            'reason':'What can we help you with today?',
        }
        widgets = {
            'description': forms.Textarea
        }