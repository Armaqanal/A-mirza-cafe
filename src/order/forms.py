from django import forms
from .models import OrderItem, Order


class EditOrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['total_discounted_price']


class AddOrderItemForm(EditOrderItemForm):
    class Meta(EditOrderItemForm.Meta):
        widgets = {
            'order': forms.HiddenInput(),
            'price': forms.HiddenInput(),
            'discounted_price': forms.HiddenInput(),
        }


# class EditOrderForm(forms.ModelForm):
class AddOrderForm(forms.ModelForm):
    is_paid = forms.BooleanField(initial=True, widget=forms.HiddenInput())

    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'is_paid': forms.HiddenInput(),
            'total_order_item_prices': forms.HiddenInput()

        }


class TotalSalesFilter(forms.Form):
    TIME_CHOICES = [
        ('year', 'Year'),
        ('year|month', 'Year and Month'),
        ('year|month|day', 'Year, Month, and Day'),
    ]

    time_choice = forms.ChoiceField(choices=TIME_CHOICES)
