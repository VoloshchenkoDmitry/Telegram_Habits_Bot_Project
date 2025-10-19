from celery import shared_task
from django.utils import timezone
import asyncio
from .models import Habit
from telegram_bot.bot import HabitBot


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках"""
    now = timezone.now()
    current_time = now.time()

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    ).select_related('user')

    bot = HabitBot()

    for habit in habits:
        if habit.user.telegram_chat_id:
            message = create_reminder_message(habit)
            asyncio.run(send_telegram_message(bot, habit.user.telegram_chat_id, message))


async def send_telegram_message(bot, chat_id, message):
    """Асинхронная отправка сообщения в Telegram"""
    try:
        await bot.send_reminder(chat_id, message)
        return True
    except Exception as e:
        print(f"Failed to send message to {chat_id}: {e}")
        return False


def create_reminder_message(habit):
    base_message = (
        f"🔔 Напоминание о привычке!\n\n"
        f"📌 Действие: {habit.action}\n"
        f"📍 Место: {habit.place}\n"
        f"⏰ Время: {habit.time.strftime('%H:%M')}\n"
        f"⏱ Время на выполнение: {habit.execution_time} секунд"
    )

    if habit.related_habit:
        base_message += f"\n\n🎁 После выполнения: {habit.related_habit.action}"
    elif habit.reward:
        base_message += f"\n\n🎁 Вознаграждение: {habit.reward}"

    return base_message