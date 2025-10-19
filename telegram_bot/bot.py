import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from django.conf import settings

logger = logging.getLogger(__name__)


class HabitBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.username = settings.TELEGRAM_BOT_USERNAME
        self.name = settings.TELEGRAM_BOT_NAME

        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")

        self.application = Application.builder().token(self.token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("habits", self.list_habits))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        message = (
            f"👋 Привет, {user.first_name}!\n\n"
            f"Я бот *{self.name}* - твой помощник в формировании привычек! 💪\n\n"
            "📋 *Что я умею:*\n"
            "• Напоминать о твоих привычках\n"
            "• Помогать отслеживать прогресс\n"
            "• Мотивировать на регулярное выполнение\n\n"
            "🔧 *Чтобы начать получать напоминания:*\n"
            "1. Скопируй свой ID чата: \n"
            f"`{update.effective_chat.id}`\n"
            "2. Добавь его в настройках профиля в приложении\n\n"
            "ℹ️ Используй /help для списка всех команд"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = (
            f"🛠 *Доступные команды:*\n\n"
            "/start - Начать работу с ботом\n"
            "/help - Показать это сообщение\n"
            "/habits - Показать сегодняшние привычки\n\n"
            "💡 *Совет:* Не забудь добавить свой Chat ID в настройках приложения!\n"
            f"Твой Chat ID: `{update.effective_chat.id}`"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

    async def list_habits(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать привычки на сегодня"""
        # Здесь можно добавить логику для получения привычек пользователя
        message = (
            "📅 *Твои привычки на сегодня:*\n\n"
            "• 08:00 - Зарядка (15 минут)\n"
            "• 12:00 - Обеденная прогулка (10 минут)\n"
            "• 19:00 - Чтение книги (30 минут)\n\n"
            "🎯 *Выполнено:* 1/3\n"
            "🔥 *Продолжай в том же духе!*"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 Я понимаю только команды. Используй /help для списка доступных команд."
        )

    async def send_reminder(self, chat_id: int, message: str):
        try:
            await self.application.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logger.info(f"Message sent to {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message to {chat_id}: {e}")
            return False

    def run(self):
        logger.info(f"Starting bot: {self.name} (@{self.username})")
        self.application.run_polling()