from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser


# Create your tests here.
class SigninTest(APITestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user('email@mail.ru', '1234')
        self.user.save()

    def tearDown(self) -> None:
        self.user.delete()

    def test_create_user(self):
        url = '/user/users/'
        data = {'email': 'email@gmail.com',
                'password': '12345678Qw'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_correct(self):
        user = authenticate(email='email@mail.ru', password='1234')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_email(self):
        user = authenticate(email='wrong', password='1234')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(email='email@mail.ru', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
