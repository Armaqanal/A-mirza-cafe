# from datetime import datetime
#
# from django import forms
#
#
# class CustomerOrder(forms.Form):
#     customer_name = forms.CharField(max_length=100)
#     customer_email = forms.EmailField()
#     products = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
#     total_amount = forms.DecimalField(max_digits=10, decimal_places=2)
#     order_date = forms.DateTimeField(initial=datetime.now)
#     status = forms.ChoiceField(initial='pending', choices=[('pending', 'confirmed')])
#     pr_date = forms.DateTimeField(initial=datetime.now)
#     ex_date = forms.DateTimeField(initial=datetime.now)
#
#
# class Product(forms.Form):
#     name = forms.CharField(max_length=100)
#     description = forms.CharField(widget=forms.Textarea, null=True, blank=True)
#     price = forms.DecimalField(max_digits=10, decimal_places=2)
#     quantity = forms.IntegerField(min_value=0, initial=0)
#     created_at = forms.DateTimeField(auto_now_add=True)
#     updated_at = forms.DateTimeField(auto_now=True)
