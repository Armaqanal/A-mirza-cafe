from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer, Staff


class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email']


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ['email']


class StaffCreationForm(UserCreationForm):
    class Meta:
        model = Staff
        fields = '__all__'


class StaffChangeForm(UserChangeForm):
    class Meta:
        model = Staff
        fields = '__all__'
