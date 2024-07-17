from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Sum

from accounts.models import DateFieldsMixin, Customer
from menu.models import MenuItem
from .managers import OrderManager


class Order(DateFieldsMixin, models.Model):
    total_order_item_prices = models.PositiveIntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    objects = OrderManager()

    def calculate_total_order_item_price(self):
        self.total_order_item_prices = self.order_items.aggregate(sum=Sum('total_discounted_price'))['sum']

    def save(self, *args, **kwargs):
        if self.pk:
            self.calculate_total_order_item_price()
        super().save(*args, **kwargs)

    # TODO: order_item's price must be refreshed all the time until the order get paid

    def __str__(self):
        return f"Order No: {self.id}"


class OrderItem(DateFieldsMixin, models.Model):
    price = models.PositiveIntegerField(default=0)
    discounted_price = models.PositiveIntegerField(default=0, blank=True)
    quantity = models.PositiveSmallIntegerField(default=0, blank=True,
                                                validators=[MaxValueValidator(100)])
    total_discounted_price = models.PositiveIntegerField(default=0, blank=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
    )

    def update_from_cleaned_data(self, cleaned_data: dict):
        self.price = cleaned_data['price']
        self.discounted_price = cleaned_data['discounted_price']
        self.quantity = cleaned_data['quantity']
        self.menu_item = cleaned_data['menu_item']
        self.order = cleaned_data['order']
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.menu_item.price
            self.discounted_price = self.menu_item.discounted_price
        self.total_discounted_price = self.quantity * self.discounted_price
        # TODO: don't let the discounted_price to become greater than 'Price' in updates
        super().save(*args, **kwargs)
        self.order.save()
