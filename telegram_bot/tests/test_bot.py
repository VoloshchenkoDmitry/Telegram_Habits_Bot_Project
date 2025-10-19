from django.test import TestCase
from unittest.mock import Mock, patch, AsyncMock
from telegram import Update, Message, Chat, User as TelegramUser
from telegram.ext import ContextTypes
from telegram_bot.bot import HabitBot


class HabitBotTest(TestCase):

    def setUp(self):
        self.bot = HabitBot()

        # Mock objects for Telegram
        self.mock_chat = Mock(spec=Chat)
        self.mock_chat.id = 123456789

        self.mock_telegram_user = Mock(spec=TelegramUser)
        self.mock_telegram_user.first_name = "Test"

        self.mock_message = Mock(spec=Message)
        self.mock_message.chat = self.mock_chat
        self.mock_message.from_user = self.mock_telegram_user

        self.mock_update = Mock(spec=Update)
        self.mock_update.message = self.mock_message
        self.mock_update.effective_chat = self.mock_chat
        self.mock_update.effective_user = self.mock_telegram_user

        self.mock_context = Mock(spec=ContextTypes.DEFAULT_TYPE)

    @patch('telegram_bot.bot.Application')
    def test_bot_initialization(self, mock_app):
        """Тест инициализации бота"""
        bot = HabitBot()
        self.assertIsNotNone(bot.application)
        mock_app.builder().token().build.assert_called_once()

    @patch('telegram_bot.bot.Application')
    async def test_start_command(self, mock_app):
        """Тест команды /start"""
        # Mock the reply_text method
        self.mock_message.reply_text = AsyncMock()

        await self.bot.start(self.mock_update, self.mock_context)

        # Check that reply_text was called with correct message
        self.mock_message.reply_text.assert_called_once()
        call_args = self.mock_message.reply_text.call_args[0][0]
        self.assertIn("Привет", call_args)
        self.assertIn("123456789", call_args)  # chat_id

    @patch('telegram_bot.bot.Application')
    async def test_help_command(self, mock_app):
        """Тест команды /help"""
        self.mock_message.reply_text = AsyncMock()

        await self.bot.help(self.mock_update, self.mock_context)

        self.mock_message.reply_text.assert_called_once()
        call_args = self.mock_message.reply_text.call_args[0][0]
        self.assertIn("/start", call_args)
        self.assertIn("/help", call_args)

    @patch('telegram_bot.bot.Application')
    async def test_handle_message(self, mock_app):
        """Тест обработки обычных сообщений"""
        self.mock_message.reply_text = AsyncMock()

        await self.bot.handle_message(self.mock_update, self.mock_context)

        self.mock_message.reply_text.assert_called_once_with(
            "Я понимаю только команды. Используй /help для списка доступных команд."
        )

    @patch('telegram_bot.bot.Application')
    async def test_send_reminder_success(self, mock_app):
        """Тест успешной отправки напоминания"""
        # Mock the bot's send_message method
        mock_bot_instance = Mock()
        mock_bot_instance.send_message = AsyncMock()
        self.bot.application.bot = mock_bot_instance

        message = "Тестовое сообщение"
        chat_id = 123456789

        result = await self.bot.send_reminder(chat_id, message)

        self.assertTrue(result)
        mock_bot_instance.send_message.assert_called_once_with(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown'
        )

    @patch('telegram_bot.bot.Application')
    async def test_send_reminder_failure(self, mock_app):
        """Тест неудачной отправки напоминания"""
        mock_bot_instance = Mock()
        mock_bot_instance.send_message = AsyncMock(side_effect=Exception("Telegram error"))
        self.bot.application.bot = mock_bot_instance

        message = "Тестовое сообщение"
        chat_id = 123456789

        result = await self.bot.send_reminder(chat_id, message)

        self.assertFalse(result)

    @patch('telegram_bot.bot.Application')
    def test_run_bot(self, mock_app):
        """Тест запуска бота"""
        mock_app_instance = Mock()
        mock_app.builder().token().build.return_value = mock_app_instance

        bot = HabitBot()
        bot.run()

        mock_app_instance.run_polling.assert_called_once()