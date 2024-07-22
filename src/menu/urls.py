from django.urls import path

from . import views

urlpatterns = [

    path('menu/<slug:slug>/', views.MenuListView.as_view(), name='menu'),

    # staff specific views
    path('manage/category/list/', views.CategoryListView.as_view(), name='manage-category-list'),
    path('manage/category/<slug:slug>/detail', views.CategoryDetailView.as_view(), name='category-detail'),
    path('manage/menu-item/add/', views.MenuItemCreateView.as_view(), name='manage-menu-item-add'),
    path('manage/category/<slug:category_slug>/menu-item/<slug:slug>/update/', views.MenuItemUpdateView.as_view(),
         name='manage-menu-item-update'),
    path('manage/category/<slug:category_slug>/menu-item/<slug:slug>/delete/', views.MenuItemDeleteView.as_view(),
         name='manage-menu-item-delete'),

    path('manage/category/create/', views.CategoryCreateView.as_view(), name='manage-category-create'),
    path('manage/category/<slug:slug>/update/', views.CategoryUpdateView.as_view(), name='manage-category-update'),
    path('manage/category/<slug:slug>/delete/', views.CategoryDeleteView.as_view(), name='manage-category-delete'),

]
