from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            email='test@user.com',
            password='testpass123'
        )

        # Создаем приятную привычку
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Читать книгу',
            is_pleasant=True,
            execution_time=120
        )

    def test_habit_creation(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Спортзал',
            time='10:00:00',
            action='Тренироваться',
            is_pleasant=False,
            execution_time=90,
            is_public=True
        )

        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.place, 'Спортзал')
        self.assertEqual(habit.action, 'Тренироваться')
        self.assertFalse(habit.is_pleasant)
        self.assertEqual(habit.execution_time, 90)
        self.assertTrue(habit.is_public)
        self.assertIsNotNone(habit.created_at)

    def test_execution_time_validation(self):
        """Тест валидации времени выполнения"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Тест',
            execution_time=121
        )

        with self.assertRaises(ValidationError) as context:
            habit.full_clean()

        self.assertIn('execution_time', str(context.exception))