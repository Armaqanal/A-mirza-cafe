from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('submit-order/<str:selected_category>/<int:menu_item_id>/',
         views.add_menu_item_to_cart,
         name='add-menu-item-to-cart'
         ),
    path('customer/orders/', views.customer_orders_view, name='customer_orders'),

    # order-management
    path('orders/', views.ManageOrderView.as_view(), name='manage-orders'),
    path('manage/order/add/', views.OrderCreateView.as_view(), name='add-order'),
    path('manage/order/<int:pk>/edit', views.OrderUpdateView.as_view(), name='edit-order'),
    path('manage/order/<int:pk>/delete/', views.DeleteOrderView.as_view(), name='delete-order'),

    # order-item-management
    path('manage/order/<int:order_id>/order-item/', views.ManageOrderItemsListView.as_view(),
         name='manage-order-items'),
    path('manage/order/<int:order_id>/order-item/add/', views.OrderItemCreateView.as_view(),
         name='add-order-item'),
    path('manage/order/<int:order_id>/order-item/<int:pk>/edit/', views.EditOrderItemView.as_view(),
         name='edit-order-item'),
    path('manage/order/<int:order_id>/order-item/<int:pk>/delete/',
         views.DeleteOrderItemView.as_view(), name='delete-order-item'),

    # manage-dashboard
    path('manage-dashboard/', views.total_sales_by_date, name='manage-dashboard'),
    path('manage-dashboard/sales-by-y', views.total_sales_by_year_csv, name='total_sales_by_year_csv'),
    path('manage-dashboard/sales-by-y-m', views.total_sales_by_month_year_csv, name='total_sales_by_month_year_csv'),
    path('manage-dashboard/sales-by-y-m-d', views.total_sales_by_year_month_day_csv,
         name='total_sales_by_year_month_day_csv'),

    # cbv order/order item
    path('order/add', views.AddOrderView.as_view(), name='create-order-form'),
    path('edit/<int:order_id>/', views.EditOrderView.as_view(), name='edit-order'),
]
