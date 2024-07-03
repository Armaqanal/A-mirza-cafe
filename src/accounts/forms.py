# from django.contrib.auth import authenticate
from django import forms

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, max_length=63)
    email = forms.EmailField(max_length=90)
    phone_number = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number']
        widgets = {
            'password': forms.PasswordInput()
        }
