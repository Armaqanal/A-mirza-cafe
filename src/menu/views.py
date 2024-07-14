from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .forms import AddMenuItem, AddCategoryForm
from .models import MenuCategory, MenuItem




# TODO: View to show recent restaurants
# TODO: View for food party


def manage_view(request):
    return render(request, 'menu/manage.html')


# *****************************Category_create_view_by_staff**************************
# @login_required
class CategoryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "menu.add_menucategory"
    model = MenuCategory
    form_class = AddCategoryForm
    template_name = 'menu/category_form.html'

    def has_permission(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseRedirect(
            reverse_lazy('accounts:register'))


# *************************************MenuItem_create_view_by_staff*********************
class MenuItemCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "menu.add_menuitem"
    model = MenuItem
    form_class = AddMenuItem
    template_name = 'menu/menuitem_form.html'

    # login_url = reverse_lazy('accounts:register')

    def has_permission(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect(
            reverse_lazy('accounts:register'))


# **************************************Menu***********************************************
class MenuListView(ListView):
    template_name = 'menu/menu_list.html'
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
