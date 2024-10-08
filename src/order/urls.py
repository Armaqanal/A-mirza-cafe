from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('submit-order/<str:selected_category>/<int:menu_item_id>/',
         views.add_menu_item_to_cart,
         name='add-menu-item-to-cart'
         ),

    # order-management
    path('manage-orders/', views.manage_orders, name='manage-orders'),
    path('manage-orders/add-order', views.add_order, name='add-order'),
    path('manage-orders/edit-order/<int:order_id>/', views.edit_order, name='edit-order'),
    path('manage-orders/delete-order/<int:order_id>/', views.delete_order, name='delete-order'),

    # order-item-management
    path('manage-orders/<int:order_id>/manage-order-items/', views.manage_order_items, name='manage-order-items'),
    path('manage-orders/<int:order_id>/manage-order-items/add-order-item/', views.add_order_item,
         name='add-order-item'),
    path('manage-orders/<int:order_id>/manage-order-items/<int:order_item_id>/edit-order-item/', views.edit_order_item,
         name='edit-order-item'),
    path('manage-orders/<int:order_id>/manage-order-items/<int:order_item_id>/delete-order-item/',
         views.delete_order_item, name='delete-order-item'),
]
