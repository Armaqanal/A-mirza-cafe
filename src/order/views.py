from django.shortcuts import render, redirect, get_object_or_404
from menu.models import MenuItem
from user.models import Customer

from .forms import EditOrderItemForm, AddOrderItemForm, AddOrderForm
from .models import Order, OrderItem


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


def manage_orders(request):
    orders = Order.objects.select_related('customer').filter(is_paid=True).order_by('-id')
    context = {
        "orders": orders
    }
    return render(request, 'order/manage_orders.html', context)


def add_order(request):
    form = AddOrderForm()
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-orders')

    context = {
        'form': form
    }
    return render(request, 'order/order_form.html', context)


def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = AddOrderForm(instance=order)
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            order.update_from_cleaned_data(form.cleaned_data)
            return redirect('manage-orders')
    context = {
        'order_id': order_id,
        'form': form
    }
    return render(request, 'order/order_form.html', context)


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('manage-orders')


# Manage orders
def manage_order_items(request, order_id):
    order_items = OrderItem.objects.select_related('menu_item').filter(order=order_id).order_by('-id')
    context = {
        'order_id': order_id,
        'order_items': order_items
    }
    return render(request, 'order/manage_order_items.html', context)


def add_order_item(request, order_id):
    order = Order.objects.get(id=order_id)
    form = AddOrderItemForm(initial={'order': order, 'quantity': 1})
    if request.method == 'POST':
        form = AddOrderItemForm(request.POST)
        if form.is_valid():
            print('*' * 50, form.cleaned_data)
            order_item = form.save()
            return redirect('manage-order-items', order_item.order_id)
    context = {
        'order_id': order_id,
        'form': form
    }
    return render(request, 'order/order_item_form.html', context)


def edit_order_item(request, order_id, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    form = EditOrderItemForm(instance=order_item)
    if request.method == 'POST':
        form = EditOrderItemForm(request.POST)
        if form.is_valid():
            order_item.update_from_cleaned_data(form.cleaned_data)
            return redirect('manage-order-items', order_item.order_id)
    context = {
        'order_id': order_id,
        'order_item_id': order_item_id,
        'form': form
    }
    return render(request, 'order/order_item_form.html', context)


def delete_order_item(request, order_id, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    order_item.delete()
    return redirect('manage-order-items', order_item.order_id)
