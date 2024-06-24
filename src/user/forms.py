from django.contrib.auth import get_user_model
from django.forms import forms


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "password")
        widgets = {
            "password": forms.PasswordInput(), }
