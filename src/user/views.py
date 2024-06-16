from django.shortcuts import render
from .models import Customer, Staff


def home(request):
    return render(request, 'website/pages/home.html')


def about(request):
    return render(request, 'website/pages/about.html')


def book(request):
    return render(request, 'website/pages/book.html')


def menu(request):
    return render(request, 'menu/menu.html')


def staff_profile(request, staff_username=None):
    staff = Staff.objects.get(username=staff_username)
    context = {"staff": staff}
    return render(request, 'user/staff/staff.html', context)


def all_staffs(request):
    colors = ["#b1dfbb", '#fcf6bd', '#7abaff', '#e76f51', '#2a9d8f', '#e4c1f9', '#81b29a', '#f77f00']
    all_staffs = Staff.objects.all()
    context = {
        "all_staffs": all_staffs,
        "colors": colors
    }
    return render(request, 'user/staff/all_staffs.html', context)


def customer(request):
    return render(request, 'user/customer.html', {})


def cart(request):
    return render(request, 'order/cart.html', {})


def order(request):
    return render(request, 'order/order.html', {})
