from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import Token

from users.views import UserViewSet


class UserSerializerTests(APITestCase):
    def test_create_user(self):

        User = get_user_model()  # Получаем актуальную модель пользователя
        data = {
            'email': 'testuser@example.com',
            'telegram_id': 'testuser',
            'password': 'testpassword',
        }

        url = reverse('users:user_create')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')
        self.assertEqual(User.objects.get().telegram_id, 'testuser')

    def test_create_user_with_invalid_data(self):

        User = get_user_model()  # Получаем актуальную модель пользователя
        data = {
            'email': 'invalidemail',
            'telegram_id': 'testuser',
            'password': 'testpassword',
        }

        url = reverse('users:user_create')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_with_no_telegram_id(self):

        User = get_user_model()  # Получаем актуальную модель пользователя
        data = {
            'email': 'invalidemail',
            'password': 'testpassword',
        }

        url = reverse('users:user_create')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_partial_update_user(self):
        """
        Ensure UserViewSet can partially update a user.
        """
        User = get_user_model()  # Получаем актуальную модель пользователя
        user = User.objects.create(email='testuser@example.com', telegram_id='testuser', password='testpassword')
        url = reverse('users:user_patch', args=[user.id])
        data = {
            'email': 'updateduser@example.com',
        }

        self.client.force_authenticate(user=user)  # Аутентификация пользователя

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()  # Обновляем объект пользователя из базы данных
        self.assertEqual(user.email, 'updateduser@example.com')

    def test_create_user_no_email(self):
        """
        Test creating a user without email raises a ValueError.
        """
        User = get_user_model()  # Получаем актуальную модель пользователя
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='testpassword')
