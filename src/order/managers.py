from django.db import models


class OrderManager(models.Manager):
    def get_unpaid_order(self, customer_id):
        qs = self.get_queryset()
        last_unpaid_order, new_unpaid_order = qs.get_or_create(customer_id=customer_id, is_paid=False)
        return last_unpaid_order or new_unpaid_order
