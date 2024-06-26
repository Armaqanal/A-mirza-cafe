from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Sum
from menu.models import MenuItem
from user.models import DateFieldsMixin, Customer


class Order(DateFieldsMixin, models.Model):
    total_order_item_prices = models.PositiveIntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def calculate_total_order_item_price(self):
        self.total_order_item_prices = self.order_items.aggregate(sum=Sum('total_discounted_price'))['sum']

    @classmethod
    def get_unpaid_order(cls, customer_id=61):
        """"""
        last_unpaid_order, new_unpaid_order = cls.objects.get_or_create(customer_id=customer_id, is_paid=False)
        return last_unpaid_order or new_unpaid_order

    def save(self, *args, **kwargs):
        if self.pk:
            self.calculate_total_order_item_price()
        super().save(*args, **kwargs)

    # TODO: order_item's price must be refreshed all the time until the order get paid


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

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price
        self.discounted_price = self.menu_item.discounted_price
        self.total_discounted_price = self.quantity * self.discounted_price
        super().save(*args, **kwargs)
        self.order.save()
