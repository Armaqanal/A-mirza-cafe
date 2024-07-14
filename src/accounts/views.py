from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from . import forms
from .forms import CustomerRegisterForm
from .models import Customer, Staff

User = get_user_model()


class AMirzaLoginView(LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('website-home')
    authentication_form = forms.LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super(AMirzaLoginView, self).form_valid(form)
        messages.success(self.request, f"Welcome dear '{str(self.request.user)}'")
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super(AMirzaLoginView, self).form_invalid(form)


class AMirzaLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('website-home')


class RegisterView(CreateView):
    model = Customer
    template_name = 'accounts/register.html'
    form_class = CustomerRegisterForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(self.request, f"Your account has been created successfully!")
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super(RegisterView, self).form_invalid(form)


class CustomerProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/customer/customer_profile.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerProfileView, self).get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer, id=self.request.user.id)
        return context


class StaffProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/staff/staff_profile.html'

    def get_context_data(self, **kwargs):
        context = super(StaffProfileView, self).get_context_data(**kwargs)
        context['staff'] = get_object_or_404(Staff, id=self.request.user.id)
        return context


class SuperuserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_profile.html'


def all_staffs_view(request):
    colors = ["#b1dfbb", '#fcf6bd', '#7abaff', '#e76f51', '#2a9d8f', '#e4c1f9', '#81b29a', '#f77f00']
    all_staffs = Staff.objects.all()
    context = {
        "all_staffs": all_staffs,
        "colors": colors
    }
    return render(request, 'accounts/staff/all_staffs.html', context)


def all_customers_view(request):
    colors = ["#b1dfbb", '#fcf6bd', '#7abaff', '#e76f51', '#2a9d8f', '#e4c1f9', '#81b29a', '#f77f00']
    all_customers = Customer.objects.all()
    context = {
        "all_customers": all_customers,
        "colors": colors
    }
    return render(request, 'accounts/customer/all_customers.html', context)
