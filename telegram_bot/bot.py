import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from django.conf import settings

logger = logging.getLogger(__name__)


class HabitBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.application = Application.builder().token(self.token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        message = (
            f"Привет, {user.first_name}!\n\n"
            "Я бот для напоминаний о привычках.\n"
            "Используй команду /help для списка доступных команд."
        )
        await update.message.reply_text(message)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = (
            "Доступные команды:\n"
            "/start - Начать работу с ботом\n"
            "/help - Показать это сообщение"
        )
        await update.message.reply_text(message)

    def run(self):
        self.application.run_polling()

    async def send_reminder(self, chat_id: int, message: str):
        try:
            await self.application.bot.send_message(
                chat_id=chat_id,
                text=message
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send message to {chat_id}: {e}")
            return False