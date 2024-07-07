from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
# from user.models import Customer
from . import forms
from .forms import CustomerRegisterForm
# from .models import User
# from django.db.models import Q
# from django.views.decorators.csrf import csrf_exempt


def login_view(request):
    if request.user.is_authenticated:
        return redirect('website-home')

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # user = Customer.objects.get(username=form.cleaned_data['username'])
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                request.session['username'] = user.username

                response = redirect('website-home')
                response.set_cookie(
                    'username',
                    form.cleaned_data['username'])
                return response

            # else:
            #     return HttpResponse('invalid login')
        else:
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')  # context={'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('website-home')


class RegisterView(View):
    form_class = CustomerRegisterForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class()
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            print('*' * 200, form)
            try:
                form.save()
            except ValueError:
                form.errors['No username'] = 'Username, Email or password is needed'
            else:
                return redirect('accounts:login')
        for error, message in form.errors.items():
            messages.error(request, message)

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


# @csrf_exempt
def user_login_view(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('website.home')
    else:
        form = forms.UserLoginForm()
    return render(request, 'accounts/user_login.html', {'form': form})
