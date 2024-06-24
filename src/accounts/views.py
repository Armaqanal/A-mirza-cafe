from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
                # Redirect to a success page.
            else:
                return HttpResponse('Invalid login')
        else:
            print(form.errors)
            # Return an 'invalid login' error message.
            return HttpResponse(' invalid login')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    pass


def signup_view(request):
    pass
