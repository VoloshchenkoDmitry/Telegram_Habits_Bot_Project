from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from habits.models import Habit
from habits.validators import HabitValidator

User = get_user_model()


class HabitValidatorTest(TestCase):

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

    def test_validate_execution_time_valid(self):
        """Тест валидации времени выполнения (валидный случай)"""
        data = {
            'place': 'Парк',
            'time': '09:00:00',
            'action': 'Бегать',
            'execution_time': 120
        }

        validator = HabitValidator(data)
        # Не должно вызывать исключение
        validator.validate()

    def test_validate_execution_time_invalid(self):
        """Тест валидации времени выполнения (невалидный случай)"""
        data = {
            'place': 'Парк',
            'time': '09:00:00',
            'action': 'Бегать',
            'execution_time': 121
        }

        validator = HabitValidator(data)
        with self.assertRaises(ValidationError):
            validator.validate()

    def test_validate_related_habit_and_reward_valid(self):
        """Тест валидации связанной привычки и вознаграждения (валидные случаи)"""
        # Только связанная привычка
        data1 = {
            'place': 'Парк',
            'time': '09:00:00',
            'action': 'Бегать',
            'execution_time': 60,
            'related_habit': self.pleasant_habit
        }

        validator1 = HabitValidator(data1)
        validator1.validate()  # Не должно вызывать исключение

        # Только вознаграждение
        data2 = {
            'place': 'Парк',
            'time': '09:00:00',
            'action': 'Бегать',
            'execution_time': 60,
            'reward': 'Кофе'
        }

        validator2 = HabitValidator(data2)
        validator2.validate()  # Не должно вызывать исключение

    def test_validate_related_habit_and_reward_invalid(self):
        """Тест валидации связанной привычки и вознаграждения (невалидный случай)"""
        data = {
            'place': 'Парк',
            'time': '09:00:00',
            'action': 'Бегать',
            'execution_time': 60,
            'related_habit': self.pleasant_habit,
            'reward': 'Кофе'  # Нельзя одновременно
        }

        validator = HabitValidator(data)
        with self.assertRaises(ValidationError):
            validator.validate()

    def test_validate_pleasant_habit_valid(self):
        """Тест валидации приятной привычки (валидный случай)"""
        data = {
            'place': 'Дом',
            'time': '10:00:00',
            'action': 'Слушать музыку',
            'is_pleasant': True,
            'execution_time': 120
        }

        validator = HabitValidator(data)
        validator.validate()  # Не должно вызывать исключение

    def test_validate_pleasant_habit_invalid(self):
        """Тест валидации приятной привычки (невалидные случаи)"""
        # С вознаграждением
        data1 = {
            'place': 'Дом',
            'time': '10:00:00',
            'action': 'Слушать музыку',
            'is_pleasant': True,
            'execution_time': 120,
            'reward': 'Награда'
        }

        validator1 = HabitValidator(data1)
        with self.assertRaises(ValidationError):
            validator1.validate()

        # Со связанной привычкой
        data2 = {
            'place': 'Дом',
            'time': '10:00:00',
            'action': 'Слушать музыку',
            'is_pleasant': True,
            'execution_time': 120,
            'related_habit': self.pleasant_habit
        }

        validator2 = HabitValidator(data2)
        with self.assertRaises(ValidationError):
            validator2.validate()

    def test_validate_related_habit_is_pleasant_valid(self):
        """Тест валидации связанной привычки (валидный случай)"""
        data = {
            'place': 'Парк',
            'time': '09:00:00',
            'action': 'Бегать',
            'execution_time': 60,
            'related_habit': self.pleasant_habit  # Приятная привычка
        }

        validator = HabitValidator(data)
        validator.validate()  # Не должно вызывать исключение

    def test_validate_related_habit_is_pleasant_invalid(self):
        """Тест валидации связанной привычки (невалидный случай)"""
        not_pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Офис',
            time='10:00:00',
            action='Работать',
            is_pleasant=False,
            execution_time=60
        )

        data = {
            'place': 'Парк',
            'time': '09:00:00',
            'action': 'Бегать',
            'execution_time': 60,
            'related_habit': not_pleasant_habit  # Не приятная привычка
        }

        validator = HabitValidator(data)
        with self.assertRaises(ValidationError):
            validator.validate()