import datetime

from django.shortcuts import render, get_object_or_404

from .models import Customer, Staff


def staff_profile(request, staff_username):
    staff = get_object_or_404(Staff, username=staff_username)
    context = {"staff": staff}
    response = render(request, 'user/staff/staff_profile.html', context)
    response.set_cookie(
        'username',
        staff_username,
        path='/',
        expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=10))
    return response


def all_staffs_view(request):
    colors = ["#b1dfbb", '#fcf6bd', '#7abaff', '#e76f51', '#2a9d8f', '#e4c1f9', '#81b29a', '#f77f00']
    all_staffs = Staff.objects.all()
    context = {
        "all_staffs": all_staffs,
        "colors": colors
    }
    return render(request, 'user/staff/all_staffs.html', context)


def customer_profile(request, customer_username):
    customer = get_object_or_404(Customer, username=customer_username)
    context = {'customer': customer}

    response = render(request, 'user/customer/customer_profile.html', context)
    response.set_cookie(
        'username',
        customer_username,
        path='/',
        expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=10))
    return response


def all_customers_view(request):
    colors = ["#b1dfbb", '#fcf6bd', '#7abaff', '#e76f51', '#2a9d8f', '#e4c1f9', '#81b29a', '#f77f00']
    all_customers = Customer.objects.all()
    context = {
        "all_customers": all_customers,
        "colors": colors
    }
    return render(request, 'user/customer/all_customers.html', context)
