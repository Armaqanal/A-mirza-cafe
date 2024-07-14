from django.urls import path
from . import views

urlpatterns = [

    # menu
    # path('menu/<slug:selected_category>?query=foodname', views.menu, name='menu-category'),

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

    # Generic Views
    path('menu/<slug:slug>/', views.MenuListView.as_view(), name='menu-category'),
    path('manage-menu/add-category/', views.CategoryCreateView.as_view(), name='add-menu-categories'),
    path('manage-menu/add-item/', views.MenuItemCreateView.as_view(), name='add-menu-item'),

]
