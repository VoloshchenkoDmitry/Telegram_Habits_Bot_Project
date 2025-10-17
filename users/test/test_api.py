from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UserAPITest(APITestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            email='test@user.com',
            password='testpass123'
        )

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        url = reverse('register')
        data = {
            'email': 'new@user.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='new@user.com').exists())

        user = User.objects.get(email='new@user.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')

    def test_user_registration_password_mismatch(self):
        """Тест регистрации с несовпадающими паролями"""
        url = reverse('register')
        data = {
            'email': 'new@user.com',
            'password': 'pass123',
            'password_confirm': 'differentpass123',
            'first_name': 'New',
            'last_name': 'User'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Пароли не совпадают', str(response.data))

    def test_user_login(self):
        """Тест входа пользователя"""
        url = reverse('login')
        data = {
            'email': 'test@user.com',
            'password': 'testpass123'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_user_login_invalid_credentials(self):
        """Тест входа с неверными учетными данными"""
        url = reverse('login')
        data = {
            'email': 'test@user.com',
            'password': 'wrongpassword'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Неверные учетные данные', str(response.data))

    def test_user_profile_retrieve(self):
        """Тест получения профиля пользователя"""
        self.client.force_authenticate(user=self.user)
        url = reverse('profile')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@user.com')

    def test_profile_access_unauthenticated(self):
        """Тест что профиль недоступен без аутентификации"""
        url = reverse('profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)