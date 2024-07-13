import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms
from .forms import CustomerRegisterForm
from .models import Customer, Staff


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




def staff_profile(request, staff_username):
    staff = get_object_or_404(Staff, username=staff_username)
    context = {"staff": staff}
    response = render(request, 'user/staff/staff_profile.html', context)
    response.set_cookie(
        'username',
        staff_username,
        path='/',
        expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=10))
    return response


def all_staffs_view(request):
    colors = ["#b1dfbb", '#fcf6bd', '#7abaff', '#e76f51', '#2a9d8f', '#e4c1f9', '#81b29a', '#f77f00']
    all_staffs = Staff.objects.all()
    context = {
        "all_staffs": all_staffs,
        "colors": colors
    }
    return render(request, 'user/staff/all_staffs.html', context)


def customer_profile(request, customer_username):
    customer = get_object_or_404(Customer, username=customer_username)
    context = {'customer': customer}

    response = render(request, 'user/customer/customer_profile.html', context)
    response.set_cookie(
        'username',
        customer_username,
        path='/',
        expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=10))
    return response


def all_customers_view(request):
    colors = ["#b1dfbb", '#fcf6bd', '#7abaff', '#e76f51', '#2a9d8f', '#e4c1f9', '#81b29a', '#f77f00']
    all_customers = Customer.objects.all()
    context = {
        "all_customers": all_customers,
        "colors": colors
    }
    return render(request, 'user/customer/all_customers.html', context)
