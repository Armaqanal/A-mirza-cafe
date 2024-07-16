from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin

from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CategoryForm, MenuItemForm
from .models import MenuCategory, MenuItem


# TODO: View to show recent restaurants
# TODO: View for food party

class MenuListView(ListView):
    """Displays Menu"""
    template_name = 'menu/menu.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        selected_category = self.kwargs.get('slug')
        if selected_category != 'all':
            queryset = queryset.filter(menu_category__slug=selected_category)
        searched_keyword = self.request.GET.get('q')
        if searched_keyword:
            queryset = queryset.filter(food_name__icontains=searched_keyword)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MenuCategory.objects.all()
        context['selected_category'] = self.kwargs.get('slug')
        return context


class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MenuCategory
    template_name = 'menu/category_list.html'
    context_object_name = 'category_list'

    def test_func(self):
        return self.request.user.is_staff


class CategoryDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'menu.view_menucategory'
    model = MenuCategory
    context_object_name = 'category'
    template_name = 'menu/category_detail.html'


class CategoryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "menu.add_menucategory"
    model = MenuCategory
    form_class = CategoryForm
    template_name = 'menu/category_form.html'
    extra_context = {'action_type': 'Adding'}

    def get_success_url(self):
        return reverse_lazy('manage-category-list')


class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'menu.change_menucategory'
    model = MenuCategory
    form_class = CategoryForm
    template_name = 'menu/category_form.html'
    extra_context = {'action_type': 'Editing'}

    def get_success_url(self):
        return reverse_lazy('manage-category-list')


class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'menu.delete_menucategory'
    model = MenuCategory

    def get_success_url(self):
        return reverse_lazy('manage-category-list')


# class MenuItemDetailView(LoginRequiredMixin, DetailView):
#     model = MenuItem
#     template_name = 'menu/menu_item_detail.html'
class MenuItemCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "menu.add_menuitem"
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/menu_item_form.html'
    extra_context = {'action_type': 'Adding'}


class MenuItemUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'menu.change_menuitem'
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/menu_item_form.html'
    extra_context = {'action_type': 'Editing'}

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'slug': self.kwargs['category_slug']})


class MenuItemDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'menu.delete_menuitem'
    model = MenuItem

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'slug': self.kwargs['category_slug']})

# todo: check permissions with customer and staff accounts
# todo: add messages
# todo: change the form style
