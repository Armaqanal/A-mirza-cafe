from django.urls import path
from . import views

urlpatterns = [

    # menu
    # path('menu/<slug:selected_category>?query=foodname', views.menu, name='menu-category'),

    # path('profile/', views.profile, name='profile'),
    # path('history/', views.order_history, name='history'),


    # staff_add_part
    path('manage-menu/', views.manage_view, name='manage-menu'),

    # Generic Views
    path('menu/<slug:slug>/', views.MenuListView.as_view(), name='menu-category'),
    path('manage-menu/add-category/', views.CategoryCreateView.as_view(), name='add-menu-categories'),
    path('manage-menu/add-item/', views.MenuItemCreateView.as_view(), name='add-menu-item'),

]

