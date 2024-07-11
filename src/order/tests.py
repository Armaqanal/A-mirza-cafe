from django.test import TestCase
from django.urls import reverse

from order.models import Order
from user.models import Customer


# from .models import Order


class AddOrderViewTests(TestCase):
    def test_add_order_get(self):
        url = reverse('add_order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "please submit the form to add your order")

    def test_add_order_post(self):
        url = reverse('add_order')
        data = {'customer_name': 'amir', 'order_number': '1', 'order_date': '2019-05-21'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "the order was successfully added")


class EditOrderViewTests(TestCase):
    def setUp(self):
        data = {
            'username': 'username_test2',
            'email': 'test@test.test2',
            'phone': '09123456782',
            'password': 'p@ssw0rd_test',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'gender': 'F',
            'date_of_birth': '1995-10-12'
        }

        customer_data = {
            **data,
            **{'balance': 800}
        }

        self.customer = Customer.objects.create(**customer_data)
        self.order = Order.objects.create(customer=self.customer)

    def test_edit_order_get(self):
        url = reverse('edit-order', kwargs={'order_id': self.order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, "200")
        self.assertContains(response, "please submit the form to edit your order")

    def test_edit_order_post(self):
        url = reverse('edit-order', kwargs={'order_id': self.order.id})
        data = {'customer_name': 'amir', 'order_number': '1', 'order_date': '2019-05-21'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,  "200")
        self.assertContains(response, "the order was successfully edit")
