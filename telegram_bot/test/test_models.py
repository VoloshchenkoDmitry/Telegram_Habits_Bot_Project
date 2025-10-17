from django.test import TestCase
from django.contrib.auth import get_user_model
from telegram_bot.models import TelegramUser

User = get_user_model()


class TelegramUserModelTest(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            email='test@user.com',
            password='testpass123'
        )

    def test_telegram_user_creation(self):
        """Тест создания Telegram пользователя"""
        telegram_user = TelegramUser.objects.create(
            user=self.user,
            telegram_chat_id=123456789,
            username='testuser'
        )

        self.assertEqual(telegram_user.user, self.user)
        self.assertEqual(telegram_user.telegram_chat_id, 123456789)
        self.assertEqual(telegram_user.username, 'testuser')
        self.assertTrue(telegram_user.is_active)
        self.assertIsNotNone(telegram_user.created_at)

    def test_telegram_user_string_representation(self):
        """Тест строкового представления"""
        telegram_user = TelegramUser.objects.create(
            user=self.user,
            telegram_chat_id=123456789
        )
        expected_str = f"{self.user.email} - {telegram_user.telegram_chat_id}"
        self.assertEqual(str(telegram_user), expected_str)