from collections import OrderedDict
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Product, Comment
from users.models import CustomUser


class CategoryTest(APITestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='category1')
        CustomUser.objects.create_superuser('superuser@mail.ru', '1234')
        CustomUser.objects.create_user('user@mail.ru', '1234')

    def tearDown(self) -> None:
        CustomUser.objects.all().delete()
        Category.objects.all().delete()

    def test_category_get(self):
        url = '/api/category/'
        response = self.client.get(url)
        self.assertEqual(response.data, [OrderedDict([('id', 1), ('name', 'category1')])])

    def test_category_create_with_superuser(self):
        url = '/api/category/'
        self.client.login(email='superuser@mail.ru', password='1234')
        response = self.client.post(url, {'name': 'category2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_create_with_user(self):
        url = '/api/category/'
        self.client.login(email='user@mail.ru', password='1234')
        response = self.client.post(url, {'name': 'category2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_create_with_none_user(self):
        url = '/api/category/'
        response = self.client.post(url, {'name': 'category2'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductTest(APITestCase):
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
        self.data = {
            'name': 'product_name2',
            'description': 'description',
            'category': self.category.id,
            'price': 500,
            'available': True,
            'discount': 25,
        }
        self.url = '/api/product/'

    def tearDown(self) -> None:
        Category.objects.all().delete()
        CustomUser.objects.all().delete()
        Product.objects.all().delete()

    def test_product_get(self):
        self.client.login(email='user@mail.ru', password='1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create_with_superuser(self):
        self.client.login(email='superuser@mail.ru', password='1234')
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_create_with_user(self):
        self.client.login(email='user@mail.ru', password='1234')
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_create_with_none_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_update_with_super_user(self):
        self.client.login(email='superuser@mail.ru', password='1234')
        response = self.client.put(self.url + '1/', self.data)
        self.assertEqual(Product.objects.get(id=1).price, 500)
        self.assertEqual(Product.objects.get(id=1).discount, 25)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_delete(self):
        self.client.login(email='superuser@mail.ru', password='1234')
        response = self.client.delete(self.url + '1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_delete_with_none_user(self):
        response = self.client.delete(self.url + '1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_with_user(self):
        self.client.login(email='user@mail.ru', password='1234')
        response = self.client.put(self.url + '1/', self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentTest(APITestCase):
    def setUp(self):
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

        self.data = {
            'rate': 5,
            'product': self.product.id,
            'content': 'some content',
        }
        Comment.objects.create(rate=5,
                               product=self.product,
                               content='some content',
                               user=self.user)
        self.url = '/api/comment/'

    def test_create_comment(self):
        self.client.login(email='user@mail.ru', password='1234')
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_comment(self):
        self.client.login(email='user@mail.ru', password='1234')
        response = self.client.put(self.url + '1/',
                                   {'rate': 3,
                                    'product': self.product.id,
                                    'content': 'no content'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(id=1).rate, 3)
        self.assertEqual(Comment.objects.get(id=1).content, 'no content')

    def test_update_comment_with_another_user(self):
        self.client.login(email='superuser@mail.ru', password='1234')
        response = self.client.put(self.url + '1/',
                                   {'rate': 3,
                                    'product': self.product.id,
                                    'content': 'no content'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

