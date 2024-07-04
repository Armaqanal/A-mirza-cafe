import os
import random
import faker
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddMenuItem, AddCategoryForm
from .models import MenuCategory, MenuItem
from user.models import Staff, Customer


def home(request):
    return render(request, 'website/pages/home.html')


def about(request):
    return render(request, 'website/pages/about.html')


def book(request):
    return render(request, 'website/pages/book.html')


def menu(request, selected_category=None):
    categories = MenuCategory.objects.all()
    if selected_category == 'all':
        menu_items = MenuItem.objects.all()
    else:
        menu_items = MenuItem.objects.filter(menu_category__slug=selected_category)
    if request.method == 'GET':
        if searched_keyword := request.GET.get('q'):
            menu_items = menu_items.filter(food_name__icontains=searched_keyword)

    context = {
        "categories": categories,
        "menu_items": menu_items,
        "selected_category": selected_category
    }
    return render(request, 'menu/menu.html', context)


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
    photos_dir = "static/user/images/profile-photo-samples/"
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
    return redirect('all-staffs')


def mock_customers(request, count=5):
    f = faker.Faker()
    photos_dir = "static/user/images/profile-photo-samples/"
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
    return redirect('all-customers')


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


# TODO: View to show recent restaurants
# TODO: View for food party


@login_required
def staff_add_category(request):
    if request.user.is_staff:
        menu_categories = MenuCategory.objects.all()
        if request.method == 'POST':
            form = AddCategoryForm(request.POST)
            if form.is_valid():
                category = form.save()
                return redirect(category.get_absolute_url())
        else:
            form = AddCategoryForm()
        context = {
            'form': form,
            'menu_categories': menu_categories
        }

        return render(request, 'menu/add_category.html', context)
        # return render(request, 'menu/menu.html', context)

    else:
        return HttpResponse("Access denied.")


@login_required
def add_menu_item(request):
    if request.user.is_staff:
        menu_items = MenuItem.objects.all()
        if request.method == 'POST':
            form = AddMenuItem(request.POST, request.FILES)
            if form.is_valid():
                # form.save()
                # return redirect('manage-menu')
                category_item = form.save()
                return redirect(category_item.get_absolute_url())
        else:
            form = AddMenuItem()
        context = {
            'form': form,
            'menu_categories': menu_items
        }
        return render(request, 'menu/add_item.html', context)

    else:
        return HttpResponse("Access denied.")
    # TODO:ACCESS DENIED PAGE FOR REDIRECT HOMEPAGE


def manage_view(request):
    return render(request, 'menu/manage.html')
