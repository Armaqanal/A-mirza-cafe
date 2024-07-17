from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages

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


class CategoryListView(PermissionRequiredMixin, ListView):
    permission_required = 'menu.view_menucategory'
    model = MenuCategory
    template_name = 'menu/category_list.html'
    context_object_name = 'category_list'
    ordering = ['label']


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

    def form_valid(self, form):
        messages.success(self.request, f"Category `{form.instance}` was successfully created.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('manage-category-list')


class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'menu.change_menucategory'
    model = MenuCategory
    form_class = CategoryForm
    template_name = 'menu/category_form.html'
    extra_context = {'action_type': 'Editing'}

    def form_valid(self, form):
        messages.info(self.request, f"Category `{form.instance}` was successfully updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('manage-category-list')


class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'menu.delete_menucategory'
    model = MenuCategory

    def form_valid(self, form):
        messages.warning(self.request, f"Category `{self.object}` was deleted.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('manage-category-list')


class MenuItemCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "menu.add_menuitem"
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/menu_item_form.html'
    extra_context = {'action_type': 'Adding'}

    def form_valid(self, form):
        messages.success(self.request, f"Menu Item `{form.instance}` was successfully created.")
        return super().form_valid(form)


class MenuItemUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'menu.change_menuitem'
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/menu_item_form.html'
    extra_context = {'action_type': 'Editing'}

    def form_valid(self, form):
        messages.info(self.request, f"Menu Item `{form.instance}` was successfully updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'slug': self.kwargs['category_slug']})


class MenuItemDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'menu.delete_menuitem'
    model = MenuItem

    def form_valid(self, form):
        messages.warning(self.request, f"Menu item `{self.object}` was deleted.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'slug': self.kwargs['category_slug']})

# todo: change the form style
