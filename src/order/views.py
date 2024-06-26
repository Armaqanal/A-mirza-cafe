import datetime

from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from user.models import Customer
from menu.models import MenuItem


def cart(request):
    username = request.COOKIES.get('username')
    customer = get_object_or_404(Customer, username=username)
    unpaid_order = Order.get_unpaid_order(customer_id=customer.id)
    unpaid_order_items = unpaid_order.order_items.all()
    context = {"unpaid_order_items": unpaid_order_items}
    return render(request, 'order/cart.html', context)


def order(request):
    print(request.COOKIES.get('username'))
    return render(request, 'order/order.html', {})


def add_menu_item_to_cart(request, selected_category=None, menu_item_id=None):
    print(request.COOKIES.get('username'), selected_category, menu_item_id)
    username = request.COOKIES.get('username')
    customer = get_object_or_404(Customer, username=username)
    # page not found cases are:
    # 1. the username is for a staff instead of a customer!
    # 2. the cookie is expired

    selected_menu_item = MenuItem.objects.get(id=menu_item_id)
    print(selected_menu_item)
    unpaid_order = Order.get_unpaid_order(customer_id=customer.id)

    # check if this item has been already selected for the 'unpaid_order',
    # if it exits get it and if it doesn't create it
    order_item = OrderItem.objects.filter(order=unpaid_order).get_or_create(menu_item=selected_menu_item,
                                                                            order=unpaid_order, quantity=1)

    return redirect('menu', selected_category)


# def add_menu_item_to_cart(request, selected_category=None, menu_item_id=None):
#     print(request.COOKIES.get('username'), selected_category, menu_item_id)
#
#     username = request.session.get('username')
#     customer = get_object_or_404(Customer, username=username)
#
#     selected_menu_item = MenuItem.objects.get(id=menu_item_id)
#     print(selected_menu_item)
#
#     # Find the online customer
#     online_customer = Customer.objects.get(is_online=True)
#
#     # Find the  online unpaid order
#     unpaid_order = Order.objects.filter(customer=online_customer, is_paid=False).first()
#
#     order_item, created = OrderItem.objects.get_or_create(
#         order=unpaid_order,
#         menu_item=selected_menu_item,
#         defaults={'quantity': 1}
#     )
#
#     if not created:
#         order_item.quantity += 1
#         order_item.save()
#
#     return redirect('menu', selected_category)


def customer_orders_view(request):
    customer_id = request.session.get('customer_id')
    customer_orders = Order.objects.filter(customer_id=customer_id).annotate(
        total_items=Count('items'),
        total_amount=Sum('item_price')
    )
    context = {
        'customer_orders': customer_orders
    }
    return render(request, 'customer_orders.html', context)






