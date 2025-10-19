from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@user.com',
            password='testpass123'
        )

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Слушать музыку',
            is_pleasant=True,
            execution_time=120
        )

    def test_habit_creation(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='09:00:00',
            action='Бегать',
            is_pleasant=False,
            execution_time=60,
            reward='Кофе',
            is_public=True
        )

        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.place, 'Парк')
        self.assertEqual(habit.action, 'Бегать')
        self.assertFalse(habit.is_pleasant)
        self.assertEqual(habit.execution_time, 60)
        self.assertEqual(habit.reward, 'Кофе')
        self.assertTrue(habit.is_public)
        self.assertEqual(habit.periodicity, 'daily')

    def test_execution_time_validation(self):
        """Тест валидации времени выполнения"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Тест',
            execution_time=121  # Превышает лимит
        )

        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_related_habit_and_reward_validation(self):
        """Тест валидации связанной привычки и вознаграждения"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Тест',
            related_habit=self.pleasant_habit,
            reward='Награда',  # Нельзя одновременно
            execution_time=60
        )

        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_with_reward_validation(self):
        """Тест валидации приятной привычки с вознаграждением"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Тест',
            is_pleasant=True,
            reward='Награда',  # У приятной привычки не может быть вознаграждения
            execution_time=60
        )

        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_related_habit_not_pleasant_validation(self):
        """Тест валидации связанной привычки, которая не является приятной"""
        not_pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Офис',
            time='10:00:00',
            action='Работать',
            is_pleasant=False,
            execution_time=60
        )

        habit = Habit(
            user=self.user,
            place='Дом',
            time='11:00:00',
            action='Тест',
            related_habit=not_pleasant_habit,  # Должна быть приятной
            execution_time=60
        )

        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_string_representation(self):
        """Тест строкового представления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Читать',
            execution_time=60
        )

        expected_str = f"{self.user}: Читать в 08:00:00"
        self.assertEqual(str(habit), expected_str)

    def test_habit_ordering(self):
        """Тест порядка привычек"""
        habit1 = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Первая привычка',
            execution_time=60
        )

        habit2 = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='09:00:00',
            action='Вторая привычка',
            execution_time=60
        )

        habits = Habit.objects.all()
        self.assertEqual(habits[0], habit2)  # Последняя созданная первая
        self.assertEqual(habits[1], habit1)