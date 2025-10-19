from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
import asyncio
from .bot import HabitBot
from habits.models import Habit

User = get_user_model()


@shared_task
def send_daily_reminders():
    """Ежедневная отправка напоминаний о привычках"""
    from habits.tasks import send_habit_reminders
    send_habit_reminders.delay()


@shared_task
def send_telegram_message_task(chat_id: int, message: str):
    """Задача для отправки сообщения в Telegram"""
    bot = HabitBot()

    try:
        # Создаем новый event loop для асинхронного выполнения
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(
            bot.send_reminder(chat_id, message)
        )
        loop.close()
        return result
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False


@shared_task
def notify_habit_created(habit_id: int):
    """Уведомление о создании новой привычки"""
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user

        if user.telegram_chat_id:
            message = (
                f"🎯 Новая привычка создана!\n\n"
                f"📌 {habit.action}\n"
                f"📍 {habit.place}\n"
                f"⏰ {habit.time.strftime('%H:%M')}\n"
                f"⏱ {habit.execution_time} секунд\n\n"
                f"Напоминания будут приходить ежедневно в указанное время."
            )

            send_telegram_message_task.delay(
                user.telegram_chat_id,
                message
            )

    except Habit.DoesNotExist:
        print(f"Habit with id {habit_id} does not exist")
    except Exception as e:
        print(f"Error notifying about habit creation: {e}")