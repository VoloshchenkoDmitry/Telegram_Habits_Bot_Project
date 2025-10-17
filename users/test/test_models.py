from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.user_data = {
            'email': 'test@user.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.email, 'test@user.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        superuser = User.objects.create_superuser(
            email='admin@admin.com',
            password='adminpass123'
        )

        self.assertEqual(superuser.email, 'admin@admin.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_email_unique(self):
        """Тест уникальности email"""
        User.objects.create_user(**self.user_data)

        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@user.com',
                password='anotherpass123'
            )

    def test_email_required(self):
        """Тест что email обязателен"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password='testpass123'
            )

    def test_user_string_representation(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'test@user.com')

    def test_telegram_chat_id_optional(self):
        """Тест что telegram_chat_id не обязателен"""
        user = User.objects.create_user(
            email='nobot@user.com',
            password='testpass123'
        )

        self.assertIsNone(user.telegram_chat_id)

    def test_telegram_chat_id_storage(self):
        """Тест хранения telegram_chat_id"""
        user = User.objects.create_user(
            email='bot@user.com',
            password='testpass123',
            telegram_chat_id=123456789
        )

        self.assertEqual(user.telegram_chat_id, 123456789)