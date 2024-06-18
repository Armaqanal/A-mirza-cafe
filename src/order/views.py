from django.shortcuts import render


def cart(request):
    return render(request, 'order/cart.html', {})


def order(request):
    return render(request, 'order/order.html', {})
