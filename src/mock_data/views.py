import os
import random

import faker
from django.shortcuts import redirect

from accounts.models import Staff, Customer
from menu.models import MenuCategory, MenuItem

LABEL_LIST = ['Iced Coffee', 'Hot Coffee', 'Fruit Juice', 'Burger', 'Pizza', 'Pasta', 'Fries']


def mock_all(request):
    mock_customers(request)
    mock_staffs(request)
    mock_menu_category(request)
    mock_menu_item(request)
    return redirect('website-home')


def mock_menu_category(request):
    for label in LABEL_LIST:
        new_cat = MenuCategory(
            label=label
        )
        new_cat.save()
    return redirect('menu-category', 'all')


def mock_menu_item(request):
    category_list = MenuCategory.objects.all()
    for category in category_list:
        photos_dir = f"static/menu/images/{category}/"
        photo_list = os.listdir(photos_dir)
        for photo_file in photo_list:
            new_item = MenuItem(
                food_name=photo_file.split('.')[0],
                description='Veniam debitis quaerat officiis quasi cupiditate quo, quisquam velit, magnam volutatem asdklu',
                price=random.randint(13, 30),
                discount=random.choice([0.0, 0.1, 0.2, 0.3]),
                inventory=random.randint(0, 20),
                menu_category=category
            )
            resource_photo_path = photos_dir + photo_file
            print('**' * 20, photo_file)
            print('**' * 20, category.label)
            print('**' * 20, resource_photo_path)
            with open(resource_photo_path, 'rb') as f_resource:
                target_photo_path = f'media/menu_item_images/{category.label}/{photo_file}'
                os.makedirs(target_photo_path.removesuffix(photo_file), exist_ok=True)
                with open(target_photo_path, 'wb') as f_target:
                    f_target.write(f_resource.read())

            new_item.image = target_photo_path.removeprefix('media/')
            new_item.save()
    return redirect('menu-category', 'all')


def mock_staffs(request, count=5):
    f = faker.Faker()
    photos_dir = "static/accounts/images/profile-photo-samples/"
    photo_list = os.listdir(photos_dir)
    for _ in range(count):
        new_staff = Staff(
            username=f.user_name(),
            password='123',
            first_name=f.first_name(),
            last_name=f.last_name(),
            # age=random.randint(8, 99),
            phone='0912' + ''.join([str(random.randint(0, 9)) for _ in range(7)]),
            email=f.email(),
            # address=f.address(),
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
    return redirect('accounts:all-staffs')


def mock_customers(request, count=5):
    f = faker.Faker()
    photos_dir = "static/accounts/images/profile-photo-samples/"
    photo_list = os.listdir(photos_dir)
    for _ in range(count):
        new_customer = Customer(
            username=f.user_name(),
            password='123',
            first_name=f.first_name(),
            last_name=f.last_name(),
            # age=random.randint(8, 99),
            phone='0912' + ''.join([str(random.randint(0, 9)) for _ in range(7)]),
            email=f.email(),
            # address=f.address(),
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
    return redirect('accounts:all-customers')


def remove_all_records(model, *args, redirect_to='website-home'):
    for model_obj in model.objects.all():
        model_obj.delete()
    return redirect(redirect_to, *args)


def remove_all(request):
    remove_all_staffs(request)
    remove_all_customers(request)
    remove_all_menu_items(request)
    return remove_all_categories(request)


def remove_all_menu_items(request):
    return remove_all_records(MenuItem)


def remove_all_categories(request):
    return remove_all_records(MenuCategory)


def remove_all_staffs(request):
    return remove_all_records(Staff)


def remove_all_customers(request):
    return remove_all_records(Customer)
