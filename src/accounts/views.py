from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
# from user.models import Customer
from . import forms
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


def signup_view(request):
    pass


# @csrf_exempt
def user_login_view(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phone_number']
        user = authenticate(email=email, password=password, phone_number=phone_number)
        if user is not None:
            login(request, user)
            messages.success(request, 'you do success login.')
            return redirect('website/home')
    else:
        form = forms.UserLoginForm()
    return render(request, 'accounts/user_login.html', {'form': form})