from django.contrib.auth import get_user_model
from django import forms

#
# class UserLoginForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ("username", "password")
#         widgets = {
#             "password": forms.PasswordInput(), }
# authentication/forms.py


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)
