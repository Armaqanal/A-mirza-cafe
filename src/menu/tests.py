from django.test import TestCase, Client
# Create your tests here.
from django.urls import reverse
from accounts.models import Staff

from .models import MenuItem, MenuCategory

'''1:permission:User staff can add
   2:MenuItem is Added
   3:Redirection to register page?'''


class MenuItemCreateViewTests(TestCase):
    def setUp(self):
        self.staff_user = Staff.objects.create(
            username='staff3_test',
            email='staff3@test.com',
            phone='1234567877',
            password='arsalan123',
            gender='M',
            salary=4000,
            role='waiter')
        self.staff_user.set_password('arsalan123')
        self.staff_user.save()
        self.client.login(username='staff3_test', password='arsalan123')

        '''test customer for redirection'''

        # self.customer_user = Customer.objects.create(username='customer_test',
        #                                              email='customer@test.com',
        #                                              phone='1234567877',
        #                                              password='arsalan123', balance=1000)
        # self.customer_user.save()
        # self.customer_user.set_password('arsalan123')
        # self.customer_user.save()
        # self.client.login(username='customer_test', password='arsalan123')

    def test_permission_required(self):
        response = self.client.get(reverse('manage-menu-item-add'))
        self.assertEqual(response.status_code, 200)

    def test_create_menu_item_post_view(self):
        data = {'food_name': 'qeyme',
                'price': 1000,
                'discount': 1.0,
                'inventory': 3,
                'menu_category': 'see'}
        response = self.client.post(reverse('manage-menu-item-add'), data=data)
        self.assertEqual(response.status_code, 200)

    # def test_redirection(self):
    #     response = self.client.get(reverse('add-menu-item'))
    #     self.assertRedirects(response, '/accounts/register/')


class CategoryCreateViewTests(TestCase):
    def setUp(self):
        print("Setting up the test case.")
        self.staff_user = Staff.objects.create(
            username='staff3_test',
            email='staff3@test.com',
            phone='1234567877',
            password='arsalan123',
            gender='M',
            salary=4000,
            role='waiter')
        self.staff_user.set_password('arsalan123')
        self.staff_user.save()
        self.client.login(username='staff3_test', password='arsalan123')

    def test_permission_required(self):
        response = self.client.get(reverse('manage-category-create'))
        self.assertEqual(response.status_code, 200)

    def test_create_category_post_view(self):
        data = {'label': 'blueberry'}
        '''follow=True -->I redirected it to the newly created category'''
        response = self.client.post(reverse('manage-category-create'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)


class MenuListViewTests(TestCase):

    def setUp(self):
        self.category1 = MenuCategory.objects.create(label='coco')
        self.category2 = MenuCategory.objects.create(label='mahi')

        self.menuitem1 = MenuItem.objects.create(
            food_name='coco sabzi', slug='coco', discount=0.1, price=1000, inventory=2,
            menu_category=self.category1
        )
        self.menuitem2 = MenuItem.objects.create(
            food_name='tila pila', slug='tila', discount=0.1, price=1000, inventory=3,
            menu_category=self.category2
        )

    def test_all_menu_item_objects(self):
        my_qs_list = [self.menuitem1, self.menuitem2]
        self.client = Client()
        response = self.client.get('/menu/all/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['menu_items'],
            my_qs_list, ordered=False)

    def test_slug_menu_categories_objects(self):
        self.client = Client()
        response = self.client.get('/menu/coco/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['categories'][0], self.category1)

    def test_q_search_keyword(self):
        self.client = Client()
        response = self.client.get('/menu/all/?q=coco sabzi')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'coco sabzi')
