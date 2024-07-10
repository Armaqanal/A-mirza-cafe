from django.test import TestCase
from django.urls import reverse
# from .models import Order


class AddOrderViewTests(TestCase):
    def test_add_order_get(self):
        url = reverse('order:add_order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "please submit the form to add your order")

    def test_add_order_post(self):
        url = reverse('order:add_order')
        data = {'customer_name': 'amir', 'order_number': '1', 'order_date': '2019-05-21'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "the order was successfully added")


class EditOrderViewTests(TestCase):
    def test_edit_order_get(self):
        url = reverse('order:edit_order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, "200")
        self.assertContains(response, "please submit the form to edit your order")

    def test_edit_order_post(self):
        url = reverse('order:edit_order')
        data = {'customer_name': 'amir', 'order_number': '1', 'order_date': '2019-05-21'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,  "200")
        self.assertContains(response, "the order was successfully edit")
