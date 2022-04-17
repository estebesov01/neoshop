from django.db.models import Sum
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from .models import OrderItem
from cart.models import CartItem
from shop.models import Category, Product
from coupon.models import Coupon


class OrderTest(APITestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='category1')
        self.superuser = CustomUser.objects.create_superuser('superuser@mail.ru', '1234')
        self.user = CustomUser.objects.create_user('user@mail.ru', '1234')
        self.product = Product.objects.create(name='product_name',
                                              description='description',
                                              category=self.category,
                                              price=1000,
                                              available=True,
                                              discount=50,
                                              supplier=self.user)
        self.product2 = Product.objects.create(name='product_name2',
                                               description='description',
                                               category=self.category,
                                               price=2000,
                                               available=True,
                                               discount=20,
                                               supplier=self.user)
        self.cart_item = CartItem.objects.create(product=self.product,
                                                 quantity=5,
                                                 user=self.user)
        self.cart_item = CartItem.objects.create(product=self.product2,
                                                 quantity=5,
                                                 user=self.user)
        self.coupon = Coupon.objects.create(code='NEOBIS',
                                            valid_from='2022-04-01 14:30:00Z',
                                            valid_to='2022-05-01 14:30:00Z',
                                            active=True,
                                            discount=50
                                            )
        self.url = '/api/order/'

    @property
    def token(self):
        response = self.client.post('/jwt/token/', {'email': 'user@mail.ru',
                                                    'password': '1234'})

        return response.json().get('access')

    def tearDown(self) -> None:
        Category.objects.all().delete()
        Product.objects.all().delete()
        CustomUser.objects.all().delete()
        Coupon.objects.all().delete()
        CartItem.objects.all().delete()

    def test_create_order(self):
        self.client.login(email='user@mail.ru', password='1234')
        response = self.client.post(self.url, {'coupon': 'NEOBIS'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 0)
        response = self.client.get(self.url + '1/')
        price_of_first_cart_item = (1000 - 1000 * 0.5) * 5
        price_of_second_cart_item = (2000 - 2000 * 0.2) * 5
        self.assertEqual(response.json().get('total_price'),
                         (price_of_first_cart_item + price_of_second_cart_item) * 0.5)


    def test_create_order_with_none_user(self):
        response = self.client.post(self.url, {'coupon': 'NEOBIS'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_with_none_cart_items(self):
        CartItem.objects.all().delete()
        self.client.login(email='user@mail.ru', password='1234')
        response = self.client.post(self.url, {'coupon': ''})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_tokens(self):
        self.client.login(HTTP_AUTHORIZATION='Token '+self.token)
        response = self.client.get('/api/category/1/')
        print(response.json().get('name'), 'category1')

