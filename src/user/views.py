import datetime

from django.shortcuts import render, get_object_or_404, HttpResponse
from menu.models import MenuItem, MenuCategory
from menu.forms import  AddMenuItem, AddCategoryForm
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


def staff_menu_categories(request):
    if request.user.is_staff:
        # return HttpResponse("Welcome, Staff User!")
        # 1:See categories
        # 2:Add categories
        # 3:see Item
        # 4:Add item
        menu_categories = MenuCategory.objects.all()
        if request.method == 'POST':
            form = AddCategoryForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = AddCategoryForm()
        context = {
            'form': form,
            'menu_categories': menu_categories
        }
        return render(request, 'staff_menu_categories.html', context)

    else:
        return HttpResponse("Access denied.")


def add_menu_item(request):
    if request.user.is_staff:
        menu_items = MenuItem.objects.all()
        if request.method == 'POST':
            form = AddMenuItem(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        else:
            form = AddMenuItem()
        context = {
            'form': form,
            'menu_categories': menu_items
        }
        return render(request, 'add_menu_item.html', context)

    else:
        return HttpResponse("Access denied.")
    # TODO:ACCESS DENIED PAGE FOR REDIRECT HOMEPAGE


