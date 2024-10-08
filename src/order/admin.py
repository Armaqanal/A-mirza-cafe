from django.contrib import admin

from order.models import Order, OrderItem


# Register your models here
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ['total_order_item_prices']  # , 'is_paid']
    list_display = ['id', 'is_paid', 'total_order_item_prices', 'customer']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    exclude = ['price', 'discounted_price', 'total_discounted_price', 'customer']
    list_display = ['price', 'discounted_price', 'quantity', 'total_discounted_price', 'menu_item', 'order']
