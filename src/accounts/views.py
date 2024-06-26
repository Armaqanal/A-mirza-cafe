from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.models import Customer
from . import forms


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


def signup_view(request):
    pass
