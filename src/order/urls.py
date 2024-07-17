from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('order/', views.MyOrdersListView.as_view(), name='my-orders'),
    path('add/menu-item/<slug:menu_item_slug>/to/cart/',
         views.AddMenuItemToCartView.as_view(),
         name='add-menu-item-to-cart'
         ),

    # order-management
    path('manage-orders/', views.ManageOrderView.as_view(), name='manage-orders'),
    path('manage-orders/add-order', views.add_order, name='add-order'),
    path('manage-orders/edit-order/<int:order_id>/', views.edit_order, name='edit-order'),
    path('manage-orders/<int:pk>/delete/', views.DeleteOrderView.as_view(), name='delete-order'),

    # order-item-management
    path('manage-orders/<int:order_id>/manage-order-items/', views.ManageOrderItemView.as_view(), name='manage-order-items'),
    path('manage-orders/<int:order_id>/manage-order-items/add-order-item/', views.add_order_item,
         name='add-order-item'),
    path('manage-orders/<int:order_id>/manage-order-items/<int:order_item_id>/edit-order-item/', views.edit_order_item,
         name='edit-order-item'),
    path('manage-orders/<int:order_id>/manage-order-items/<int:pk>/delete/',
         views.DeleteOrderItem.as_view(), name='delete-order-item'),

    # manage-dashboard
    path('manage-dashboard/', views.total_sales_by_date, name='manage-dashboard'),
    path('manage-dashboard/sales-by-y', views.total_sales_by_year_csv, name='total_sales_by_year_csv'),
    path('manage-dashboard/sales-by-y-m', views.total_sales_by_month_year_csv, name='total_sales_by_month_year_csv'),
    path('manage-dashboard/sales-by-y-m-d', views.total_sales_by_year_month_day_csv,
         name='total_sales_by_year_month_day_csv')
]
