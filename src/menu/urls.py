from django.urls import path
from . import views

urlpatterns = [
    # website
    path('', views.home, name='website-home'),
    path('about/', views.about, name='website-about'),
    path('book/', views.book, name='book'),

    # menu
    path('menu/<str:selected_category>/', views.menu, name='menu'),

    # not important
    path('mock/menu/', views.mock_menu_item, name='menu-mock'),
    path('mock/category/', views.mock_menu_category, name='category-mock'),
    path('remove/category/', views.remove_all_categories, name='remove-all-categories'),
    path('remove/menu/', views.remove_all_menu_items, name='remove-all-menu-items'),
]
