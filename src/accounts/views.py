from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from . import forms


def login_view(request):
    # form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('invalid login')
    return render(
        request, 'accounts/login.html')  #context={'form': form})


def logout_view(request):
    pass


def signup_view(request):
    pass
