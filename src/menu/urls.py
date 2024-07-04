from django.urls import path
from . import views

urlpatterns = [
    # website
    path('', views.home, name='website-home'),
    path('about/', views.about, name='website-about'),
    path('book/', views.book, name='book'),

    # menu
    # path('menu/<slug:selected_category>?query=foodname', views.menu, name='menu-category'),
    path('menu/<slug:selected_category>/', views.menu, name='menu-category'),



    # persian slug
    # re_path(r'category/(?P<slug>[\w-]+)/restaurants/$', views.category_restaurants_by_slug,
    #         name='category-slug-restaurants'),

    # not important
    path('mock/', views.mock_all, name='mock-all'),
    path('mock/staff/', views.mock_staffs, name='mock-staffs'),
    path('mock/customer/', views.mock_customers, name='mock-customer'),
    path('mock/menu/', views.mock_menu_item, name='menu-mock'),
    path('mock/category/', views.mock_menu_category, name='category-mock'),
    path('remove/', views.remove_all, name='remove-all'),
    path('remove/category/', views.remove_all_categories, name='remove-all-categories'),
    path('remove/menu/', views.remove_all_menu_items, name='remove-all-menu-items'),
    path('remove/staff/', views.remove_all_staffs, name='remove-all-staffs'),
    path('remove/customer/', views.remove_all_customers, name='remove-all-customers'),

    # staff_add_part
    path('manage-menu/', views.manage_view, name='manage-menu'),
    path('manage-menu/add-category/', views.staff_add_category, name='add-menu-categories'),
    path('manage-menu/add-item/', views.add_menu_item, name='add-menu-item'),


    path('menu/<slug:slug>/', views.menu, name='menu-category')
]
