from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPITest(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')

        self.valid_user_data = {
            'email': 'tests@example.com',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'telegram_chat_id': 123456789
        }

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        response = self.client.post(
            self.register_url,
            self.valid_user_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'tests@example.com')
        self.assertIn('id', response.data)
        self.assertNotIn('password', response.data)

    def test_user_registration_invalid_data(self):
        """Тест регистрации с невалидными данными"""
        invalid_data = {
            'email': 'invalid-email',
            'password': '123'  # Слишком короткий пароль
        }

        response = self.client.post(
            self.register_url,
            invalid_data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_token_obtain(self):
        """Тест получения JWT токена"""
        # Сначала регистрируем пользователя
        self.client.post(self.register_url, self.valid_user_data)

        # Получаем токен
        login_data = {
            'email': 'tests@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(self.token_url, login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_token_refresh(self):
        """Тест обновления JWT токена"""
        # Регистрируем и получаем refresh токен
        self.client.post(self.register_url, self.valid_user_data)

        login_response = self.client.post(self.token_url, {
            'email': 'tests@example.com',
            'password': 'testpass123'
        })

        refresh_token = login_response.data['refresh']

        # Обновляем токен
        refresh_response = self.client.post(
            self.token_refresh_url,
            {'refresh': refresh_token}
        )

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_duplicate_email_registration(self):
        """Тест регистрации с существующим email"""
        # Первая регистрация
        self.client.post(self.register_url, self.valid_user_data)

        # Вторая попытка с тем же email
        response = self.client.post(
            self.register_url,
            self.valid_user_data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)