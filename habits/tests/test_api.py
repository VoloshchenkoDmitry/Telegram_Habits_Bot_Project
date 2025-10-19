from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


class HabitAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@user.com',
            password='testpass123'
        )

        self.other_user = User.objects.create_user(
            email='other@user.com',
            password='testpass123'
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Читать книгу',
            execution_time=60,
            is_public=True
        )

        self.private_habit = Habit.objects.create(
            user=self.user,
            place='Офис',
            time='09:00:00',
            action='Работать',
            execution_time=120,
            is_public=False
        )

        self.public_habit_other = Habit.objects.create(
            user=self.other_user,
            place='Парк',
            time='10:00:00',
            action='Бегать',
            execution_time=30,
            is_public=True
        )

        self.client.force_authenticate(user=self.user)

    def test_get_habits_list(self):
        """Тест получения списка привычек пользователя"""
        url = reverse('habits-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Только привычки текущего пользователя
        self.assertEqual(response.data['results'][0]['action'], 'Работать')

    def test_create_habit(self):
        """Тест создания привычки"""
        url = reverse('habits-list')
        data = {
            'place': 'Парк',
            'time': '09:00:00',
            'action': 'Бегать',
            'execution_time': 60,
            'reward': 'Кофе'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 4)
        self.assertEqual(response.data['action'], 'Бегать')
        self.assertEqual(response.data['user'], self.user.id)

    def test_get_public_habits(self):
        """Тест получения публичных привычек"""
        url = reverse('habits-public')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должны видеть все публичные привычки, включая других пользователей
        self.assertGreaterEqual(len(response.data['results']), 2)

    def test_update_own_habit(self):
        """Тест обновления своей привычки"""
        url = reverse('habits-detail', args=[self.habit.id])
        data = {
            'place': 'Библиотека',
            'time': '08:00:00',
            'action': 'Читать книгу',
            'execution_time': 60
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, 'Библиотека')

    def test_delete_own_habit(self):
        """Тест удаления своей привычки"""
        url = reverse('habits-detail', args=[self.habit.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 2)

    def test_cannot_access_other_user_private_habit(self):
        """Тест невозможности доступа к приватной привычке другого пользователя"""
        private_habit_other = Habit.objects.create(
            user=self.other_user,
            place='Дом',
            time='11:00:00',
            action='Приватная привычка',
            execution_time=60,
            is_public=False
        )

        url = reverse('habits-detail', args=[private_habit_other.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pagination(self):
        """Тест пагинации"""
        # Создаем больше привычек для тестирования пагинации
        for i in range(10):
            Habit.objects.create(
                user=self.user,
                place=f'Место {i}',
                time='08:00:00',
                action=f'Действие {i}',
                execution_time=60
            )

        url = reverse('habits-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 5)  # PAGE_SIZE из настроек