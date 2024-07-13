from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.urls import reverse

from user.models import Customer
from .forms import LoginForm, CustomerRegisterForm

User = get_user_model()


class LoginFormTest(TestCase):
    def setUp(self):
        # we need a user in the user table because AuthenticationFrom authenticate the user in form-level!
        self.user = User.objects.create_user(username='username_test', password='p@ssw0rd_test')
        self.request_factory = RequestFactory()

    def test_login_form_valid_submission(self):
        data = {
            'username': 'username_test',
            'password': 'p@ssw0rd_test',
        }
        request = self.request_factory.post(path='/accounts/login/', data=data)
        form = LoginForm(request, request.POST)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'username_test')
        self.assertEqual(form.cleaned_data['password'], 'p@ssw0rd_test')

    def test_login_form_invalid_submission(self):
        data = {
            'username': 'username_test',
            'password': 'wrong_password',
        }
        request = self.request_factory.post(path='/accounts/login/', data=data)

        form = LoginForm(request, request.POST)
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors.get('__all__')), 0)


class CustomerRegisterFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username_test', password='p@ssw0rd_test')

    def test_customer_register_form_valid_submission(self):
        # image = SimpleUploadedFile('test.png', b"file_content", content_type='image/png')
        form = CustomerRegisterForm(
            data={
                'username': 'username_test2',
                'email': 'test@test.test2',
                'phone': '09123456782',
                'password1': 'p@ssw0rd_test',
                'password2': 'p@ssw0rd_test',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'gender': 'F',
                'date_of_birth': '1995-10-12'
            },
            # files={
            #     'photo': image,
            # }

        )
        self.assertTrue(form.is_valid())
        new_customer = form.save()
        self.assertIsInstance(new_customer, Customer)
        self.assertEqual(new_customer.username, 'username_test2')
        self.assertEqual(new_customer.email, 'test@test.test2')
        self.assertEqual(new_customer.phone, '09123456782')
        self.assertTrue(new_customer.check_password('p@ssw0rd_test'))
        self.assertEqual(new_customer.first_name, 'Jane')
        self.assertEqual(new_customer.last_name, 'Doe')
        self.assertEqual(new_customer.gender, 'F')
        self.assertEqual(new_customer.date_of_birth.strftime('%Y-%m-%d'), '1995-10-12')
        # self.assertEqual(new_customer.photo, 'profile_photos/customer/username_test2.png')

    def test_customer_register_form_invalid_submission(self):
        form = CustomerRegisterForm(
            data={
                'password1': 'p@ssw0rd_test',
                'password2': 'p@ssw0rd_test',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'gender': 'F',
                'date_of_birth': '1995-10-12'
            },

        )

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class AMirzaLoginView(TestCase):
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
        staff_data = {
            **data,
            **{'salary': 5000, 'role': 'barista'}
        }
        self.customer = Customer.objects.create(**customer_data)
        self.login_url = reverse('accounts:login')
        self.client = Client()

    def test_login_success(self):
        # get login page
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        # post login data
        data = {
            'username': 'username_test2',
            'password': 'p@ssw0rd_test'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        data = {
            'username': 'username_test2',
            'password': 'p@ssw0rd_wrong'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)


class AMirzaLogoutView(TestCase):
    ...


class RegisterView(TestCase):
    ...
