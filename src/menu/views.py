import os
import random

from django.shortcuts import render, redirect

from .models import MenuCategory, MenuItem


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
        menu_items = MenuItem.objects.filter(menu_category__label=selected_category)

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


def mock_menu_category(request):
    for label in LABEL_LIST:
        new_cat = MenuCategory(
            label=label
        )
        new_cat.save()
    return redirect('menu', 'all')


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
    return redirect('menu', 'all')


def remove_all_menu_items(request):
    for item in MenuItem.objects.all():
        item.delete()

    return redirect('menu', 'all')


def remove_all_categories(request):
    for cat in MenuCategory.objects.all():
        cat.delete()

    return redirect('menu', 'all')

# TODO: View to show recent restaurants
# TODO: View for food party
