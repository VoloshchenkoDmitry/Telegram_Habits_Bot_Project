from celery import shared_task
from django.utils import timezone
from datetime import datetime
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
    ).select_related('user__telegram')

    bot = HabitBot()

    for habit in habits:
        if hasattr(habit.user, 'telegram') and habit.user.telegram.is_active:
            message = create_reminder_message(habit)
            bot.send_reminder(habit.user.telegram.telegram_chat_id, message)


def create_reminder_message(habit):
    base_message = f"Напоминание о привычке:\n\n{habit.action}\nМесто: {habit.place}\nВремя: {habit.time}"

    if habit.related_habit:
        base_message += f"\n\nПосле выполнения: {habit.related_habit.action}"
    elif habit.reward:
        base_message += f"\n\nВознаграждение: {habit.reward}"

    base_message += f"\n\nВремя на выполнение: {habit.execution_time} секунд"
    return base_message