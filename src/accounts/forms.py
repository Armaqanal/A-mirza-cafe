from django.contrib.auth import authenticate
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=60, widget=forms.EmailInput)
    phone_number = forms.CharField(max_length=15, widget=forms.NumberInput)
    password = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=[('Man', 'Female')])
    age = forms.IntegerField(widget=forms.NumberInput)
    address = forms.CharField(max_length=100)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')
    #     password = cleaned_data.get('password')
    #     phone_number = cleaned_data.get('phone_number')
    #     # gender = cleaned_data.get('gender')
    #     # age = cleaned_data.get('age')
    #     # address = cleaned_data.get('address')
    #     user = authenticate(username=email, phone_number=phone_number, password=password)
    #     if user is not None:
    #         return user
    #     else:
    #         raise forms.ValidationError('Invalid login credentials')








