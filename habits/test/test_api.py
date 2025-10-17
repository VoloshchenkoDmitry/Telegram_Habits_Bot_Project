from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from habits.models import Habit

User = get_user_model()


class HabitAPITest(APITestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            email='test@user.com',
            password='testpass123'
        )

        self.other_user = User.objects.create_user(
            email='other@user.com',
            password='testpass123'
        )

        # Привычки текущего пользователя
        self.habit1 = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Читать книгу',
            execution_time=60,
            is_public=True
        )

        # Привычка другого пользователя
        self.other_habit = Habit.objects.create(
            user=self.other_user,
            place='Офис',
            time='10:00:00',
            action='Работать',
            execution_time=90,
            is_public=True
        )

        self.client.force_authenticate(user=self.user)

    def test_get_habits_list(self):
        """Тест получения списка привычек текущего пользователя"""
        url = reverse('habits-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], self.habit1.action)

    def test_create_habit(self):
        """Тест создания привычки"""
        url = reverse('habits-list')
        data = {
            'place': 'Спортзал',
            'time': '11:00:00',
            'action': 'Тренироваться',
            'execution_time': 90,
            'reward': 'Белок'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(Habit.objects.last().user, self.user)

    def test_get_habit_detail(self):
        """Тест получения деталей привычки"""
        url = reverse('habits-detail', args=[self.habit1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], self.habit1.action)

    def test_cannot_access_other_user_habit(self):
        """Тест что нельзя получить доступ к чужой привычке"""
        url = reverse('habits-detail', args=[self.other_habit.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habits_list(self):
        """Тест получения списка публичных привычек"""
        url = reverse('habits-public')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должны видеть публичные привычки всех пользователей
        self.assertEqual(len(response.data['results']), 2)