import datetime

from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from user.models import Customer

from menu.models import MenuItem


def cart(request):
    print('\033[93m', request.method, '\033[0m', request)
    response = render(request, 'order/cart.html', {})

    response.set_cookie('username', 'jabid', expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=10))
    return response


def order(request):
    print(request.COOKIES.get('username'))
    return render(request, 'order/order.html', {})


def submit_order(request, selected_category=None, menu_item_id=None):
    print(request.COOKIES.get('username'), selected_category, menu_item_id)
    customer_id = get_object_or_404(Customer, username=request.COOKIES.get('username')).id
    # page not found cases are:
    # 1. the username is for a staff instead of a customer!
    # 2. the cookie is expired

    selected_menu_item = MenuItem.objects.get(id=menu_item_id)
    print(selected_menu_item)
    unpaid_order = Order.get_unpaid_order(customer_id)
    OrderItem.objects.create()
    return redirect('menu', selected_category)
