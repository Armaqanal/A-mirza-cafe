from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('submit-order/<str:selected_category>/<int:menu_item_id>/',
         views.submit_order,
         name='submit-order'
         ),
    path('customer/orders/', views.customer_orders_view, name='customer_orders'),
]
