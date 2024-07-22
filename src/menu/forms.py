from django import forms
from menu.models import MenuCategory

from menu.models import MenuItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        exclude = ['slug']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        exclude = ['created_at', 'updated_at', 'slug']
        widgets = {
            'description': forms.Textarea(),
        }
