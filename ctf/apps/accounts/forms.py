from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Player


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    affiliation = forms.CharField(max_length=128, required=False, label="Affiliation (optional)")
    country = forms.CharField(max_length=64, required=False, label="Country (optional)")

    class Meta:
        model = Player
        fields = ('username', 'email', 'affiliation', 'country', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'
            field.widget.attrs['autocomplete'] = 'off'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('bio', 'avatar', 'country', 'website', 'affiliation')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'
