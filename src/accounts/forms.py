from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from user.models import Customer
from .models import User

User = get_user_model()


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control form-control-lg',
                'id': 'username'
            }
        )

        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control form-control-lg',
                'id': 'password'
            }
        )


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


class DateInput(forms.DateInput):
    input_type = 'date'


class CustomerRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-lg',
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control form-control-lg',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'id': 'lastName'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'id': 'firstName'
        })
        self.fields['gender'].widget.attrs.update({
            'class': 'form-select',
        })
        self.fields['photo'].widget.attrs.update({
            'class': 'form-control ',
        })

        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'form-control ',
        })

    def clean_username(self):
        username = self.cleaned_data['username']
        phone = self.cleaned_data.get('phone')
        email = self.cleaned_data.get('email')
        if not (username or email or phone):
            raise ValidationError(
                "Providing username, email or phone number is required.",
                code='invalid'
            )
        return username

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'photo', 'first_name', 'last_name',
                  'date_of_birth', 'gender']
        widgets = {
            'date_of_birth': DateInput
        }
