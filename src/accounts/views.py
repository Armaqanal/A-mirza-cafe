from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user.models import Customer
from . import forms
from .forms import CustomerRegisterForm


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
