from django.urls import path
from . import views

urlpatterns = [
    # website
    path('', views.home, name='website-home'),
    path('about/', views.about, name='website-about'),
    path('book/', views.book, name='book'),

    # menu
    path('menu/', views.all_food, name='menu'),
    path('menu/mock', views.mock_menu_item, name='menu-mock'),
    path('category/mock', views.mock_menu_category, name='category-mock'),
]
