from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AccountModel
from django import forms

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=6)

    class Meta:
        model = AccountModel
        fields = ('first_name', 'last_name', 'email',  'username', 'password1', 'password2', 'birthday')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password1

class LoginForm(forms.Form):
    class Meta:
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput, min_length=6)