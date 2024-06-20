import datetime

from django.shortcuts import render, redirect
from .models import Order, OrderItem


def cart(request):
    print('\033[93m', request.method, '\033[0m', request)
    response = render(request, 'order/cart.html', {})

    response.set_cookie('username', 'jabid', expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=10))
    return response


def order(request):
    print(request.COOKIES.get('username'))
    return render(request, 'order/order.html', {})


def submit_order(request, selected_category=None):
    print(request.COOKIES.get('username'))

    return redirect('menu', selected_category)
