from django.utils import timezone
from django.test import TestCase
from ..models import User, Customer, Staff, Address


class UserTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            city="Test City",
            state="Test State",
            neighborhood="Test Neighborhood",
            street="Test Street",
            alley="Test Alley",
            zip_code="123456"
        )
        self.user = User.objects.create_user(
            username='username_test',
            password='p@ssw0rd_test',
            phone='09123456789',
            email='email@test.test',
            photo='test.png',
            date_of_birth=timezone.datetime(year=2001, month=8, day=1),
            gender=User.Gender.MALE,
            address=self.address,
        )

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, "username_test")
        self.assertEqual(self.user.email, "email@test.test")
        self.assertEqual(self.user.phone, "09123456789")
        self.assertEqual(self.user.gender, User.Gender.MALE)
        self.assertEqual(self.user.address, self.address)
        self.assertTrue(self.user.check_password('p@ssw0rd_test'))
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)

    def test_user_address(self):
        self.assertEqual(self.user.address.city, "Test City")
        self.assertEqual(self.user.address.state, "Test State")
        self.assertEqual(self.user.address.neighborhood, "Test Neighborhood")
        self.assertEqual(self.user.address.street, "Test Street")
        self.assertEqual(self.user.address.alley, "Test Alley")
        self.assertEqual(self.user.address.zip_code, "123456")

    def test_user_age_property(self):
        age = timezone.now().year - 2001 - ((timezone.now().month, timezone.now().day) < (8, 1))
        self.assertEqual(self.user.age, age)

    def test_user_is_customer_property(self):
        self.assertTrue(self.user.is_customer)

    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'username_test')

        self.user.username = None
        self.assertEqual(str(self.user), "email@test.test")

        self.user.email = None
        self.assertEqual(str(self.user), "09123456789")

    def test_user_save_method(self):
        self.user.username = ''
        self.user.email = ''
        self.user.phone = ''

        self.assertRaises(ValueError, self.user.save)


class SuperUserTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            city="Test City",
            state="Test State",
            neighborhood="Test Neighborhood",
            street="Test Street",
            alley="Test Alley",
            zip_code="123456"
        )
        self.user = User.objects.create_superuser(
            username='username_test',
            password='p@ssw0rd_test',
            phone='09123456789',
            email='email@test.test',
            photo='test.png',
            date_of_birth=timezone.datetime(year=2001, month=8, day=1),
            gender=User.Gender.MALE,
            address=self.address,
        )

    def test_superuser_creation(self):
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_staff)

    def test_superuser_is_customer_property(self):
        self.assertFalse(self.user.is_customer)


class CustomerTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create_user(
            username='username_test',
            password='p@ssw0rd_test',
            phone='09123456789',
            email='email@test.test',
            photo='test.png',
            date_of_birth=timezone.datetime(year=2001, month=8, day=1),
            gender=User.Gender.MALE,
            balance=500
        )

    def test_customer_creation(self):
        self.assertIsInstance(self.customer, Customer)
        self.assertFalse(self.customer.is_superuser)
        self.assertFalse(self.customer.is_staff)
        self.assertEqual(self.customer.balance, 500)

    def test_customer_is_customer_property(self):
        self.assertTrue(self.customer.is_customer)


class StaffModelTest(TestCase):

    def setUp(self):
        self.staff = Staff.objects.create_user(
            username='username_test',
            password='p@ssw0rd_test',
            phone='09123456789',
            email='email@test.test',
            photo='test.png',
            date_of_birth=timezone.datetime(year=2001, month=8, day=1),
            gender=User.Gender.MALE,
            salary=1000,
            role=Staff.RoleType.BARISTA
        )

    def test_staff_creation(self):
        self.assertIsInstance(self.staff, Staff)
        self.assertEqual(self.staff.role, Staff.RoleType.BARISTA)
        self.assertEqual(self.staff.salary, 1000)

    def test_staff_is_staff_property(self):
        self.assertTrue(self.staff.is_staff)
