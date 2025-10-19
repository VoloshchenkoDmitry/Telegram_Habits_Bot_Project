from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTest(TestCase):

    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = User.objects.create_user(
            email='tests@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )

        self.assertEqual(user.email, 'tests@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )

        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_email_required(self):
        """Тест обязательности email"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password='testpass123'
            )

    def test_telegram_chat_id_unique(self):
        """Тест уникальности telegram_chat_id"""
        User.objects.create_user(
            email='user1@example.com',
            password='pass123',
            telegram_chat_id=12345
        )

        with self.assertRaises(Exception):
            User.objects.create_user(
                email='user2@example.com',
                password='pass123',
                telegram_chat_id=12345
            )

    def test_user_string_representation(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(
            email='tests@example.com',
            password='testpass123'
        )

        self.assertEqual(str(user), 'tests@example.com')

    def test_user_ordering(self):
        """Тест порядка пользователей по email"""
        User.objects.create_user(email='b@example.com', password='pass123')
        User.objects.create_user(email='a@example.com', password='pass123')
        User.objects.create_user(email='c@example.com', password='pass123')

        users = User.objects.all()
        self.assertEqual(users[0].email, 'a@example.com')
        self.assertEqual(users[1].email, 'b@example.com')
        self.assertEqual(users[2].email, 'c@example.com')