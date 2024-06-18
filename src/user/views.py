import os
import random

from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Staff
import faker


def staff_profile(request, staff_username):
    staff = get_object_or_404(Staff, username=staff_username)
    context = {"staff": staff}
    return render(request, 'user/staff/staff_profile.html', context)


def all_staffs_view(request):
    colors = ["#b1dfbb", '#fcf6bd', '#7abaff', '#e76f51', '#2a9d8f', '#e4c1f9', '#81b29a', '#f77f00']
    all_staffs = Staff.objects.all()
    context = {
        "all_staffs": all_staffs,
        "colors": colors
    }
    return render(request, 'user/staff/all_staffs.html', context)


def mock_staffs(request, count=5):
    valid_phone_list = ['09318923823', '09231802829', '09123334433']
    f = faker.Faker()
    photos_dir = "static/user/images/profile-photo-samples/"
    photo_list = os.listdir(photos_dir)
    for _ in range(count):
        new_staff = Staff(
            username=f.user_name(),
            password=f.password(),
            first_name=f.first_name(),
            last_name=f.last_name(),
            phone=random.choice(valid_phone_list),
            email=f.email(),
            address=f.address(),
            is_active=random.choice([True, False]),
            salary=1800,
            role=random.choice([choice_tuple[0] for choice_tuple in Staff.RoleType.choices]),
        )
        selected_photo = random.choice(photo_list)
        resource_photo_path = photos_dir + selected_photo
        with open(resource_photo_path, 'rb') as f_resource:
            target_photo_path = f'media/profile_photos/staff/{selected_photo}'
            os.makedirs(target_photo_path.removesuffix(selected_photo), exist_ok=True)
            with open(target_photo_path, 'wb') as f_target:
                f_target.write(f_resource.read())

        new_staff.photo = target_photo_path.removeprefix('media/')
        new_staff.save()
    return redirect('all-staffs')


def customer_profile(request, customer_username):
    customer = get_object_or_404(Customer, username=customer_username)
    context = {'customer': customer}

    return render(request, 'user/customer/customer_profile.html', context)


def all_customers_view(request):
    colors = ["#b1dfbb", '#fcf6bd', '#7abaff', '#e76f51', '#2a9d8f', '#e4c1f9', '#81b29a', '#f77f00']
    all_customers = Customer.objects.all()
    context = {
        "all_customers": all_customers,
        "colors": colors
    }
    return render(request, 'user/customer/all_customers.html', context)


def mock_customers(request, count=5):
    valid_phone_list = ['09318923823', '09231802829', '09123334433']
    f = faker.Faker()
    photos_dir = "static/user/images/profile-photo-samples/"
    photo_list = os.listdir(photos_dir)
    for _ in range(count):
        new_customer = Customer(
            username=f.user_name(),
            password=f.password(),
            first_name=f.first_name(),
            last_name=f.last_name(),
            phone=random.choice(valid_phone_list),
            email=f.email(),
            address=f.address(),
            is_active=random.choice([True, False]),
            balance=180,
        )
        selected_photo = random.choice(photo_list)
        resource_photo_path = photos_dir + selected_photo
        with open(resource_photo_path, 'rb') as f_resource:
            target_photo_path = f'media/profile_photos/customer/{selected_photo}'
            os.makedirs(target_photo_path.removesuffix(selected_photo), exist_ok=True)
            with open(target_photo_path, 'wb') as f_target:
                f_target.write(f_resource.read())

        new_customer.photo = target_photo_path.removeprefix('media/')
        new_customer.save()
    return redirect('all-customers')
