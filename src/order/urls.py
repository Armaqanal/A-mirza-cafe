from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('cart/pay/', views.PayCartView.as_view(), name='pay-cart'),
    path('cart-item/<int:pk>/update/', views.CartItemUpdateView.as_view(), name='cart-item-update'),
    path('cart-item/<int:pk>/delete/', views.CartItemDeleteView.as_view(), name='cart-item-delete'),
    path('order/', views.MyOrdersListView.as_view(), name='my-orders'),
    path('add/menu-item/<slug:menu_item_slug>/to/cart/',
         views.AddMenuItemToCartView.as_view(),
         name='add-menu-item-to-cart'
         ),

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
         name='total_sales_by_year_month_day_csv')
]
