from django import forms
from menu.models import MenuCategory

from menu.models import MenuItem


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = '__all__'
        widgets = {
            'label': forms.TextInput()
        }


class AddMenuItem(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'
        widgets = {
            'food_name': forms.TextInput(),
            'description': forms.Textarea(),
            'price': forms.NumberInput(),
            'discount': forms.NumberInput(),
            'inventory': forms.NumberInput(),
            'image': forms.FileInput(),
            'menu_category': forms.Select(),
        }
