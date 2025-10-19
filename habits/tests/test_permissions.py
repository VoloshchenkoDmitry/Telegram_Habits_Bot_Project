from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habits.models import Habit
from habits.permissions import IsOwner

User = get_user_model()


class IsOwnerPermissionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='owner@user.com',
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
            action='Читать',
            execution_time=60
        )

        self.permission = IsOwner()

    def test_has_object_permission_owner(self):
        """Тест разрешения для владельца объекта"""
        request = type('Request', (), {'user': self.user})()
        has_permission = self.permission.has_object_permission(
            request, None, self.habit
        )

        self.assertTrue(has_permission)

    def test_has_object_permission_not_owner(self):
        """Тест разрешения для не владельца объекта"""
        request = type('Request', (), {'user': self.other_user})()
        has_permission = self.permission.has_object_permission(
            request, None, self.habit
        )

        self.assertFalse(has_permission)


class HabitPermissionsAPITest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email='owner@user.com',
            password='testpass123'
        )

        self.other_user = User.objects.create_user(
            email='other@user.com',
            password='testpass123'
        )

        self.habit = Habit.objects.create(
            user=self.owner,
            place='Дом',
            time='08:00:00',
            action='Читать',
            execution_time=60,
            is_public=False
        )

        self.public_habit = Habit.objects.create(
            user=self.owner,
            place='Парк',
            time='09:00:00',
            action='Бегать',
            execution_time=30,
            is_public=True
        )

    def test_owner_can_access_own_habit(self):
        """Тест доступа владельца к своей привычке"""
        self.client.force_authenticate(user=self.owner)

        url = reverse('habits-detail', args=[self.habit.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_access_private_habit(self):
        """Тест запрета доступа другого пользователя к приватной привычке"""
        self.client.force_authenticate(user=self.other_user)

        url = reverse('habits-detail', args=[self.habit.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_user_can_access_public_habit_via_public_list(self):
        """Тест доступа другого пользователя к публичной привычке через список"""
        self.client.force_authenticate(user=self.other_user)

        url = reverse('habits-public')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должен видеть публичные привычки
        public_habits = [h['id'] for h in response.data['results']]
        self.assertIn(self.public_habit.id, public_habits)

    def test_anonymous_can_access_public_habits(self):
        """Тест доступа анонимного пользователя к публичным привычкам"""
        self.client.force_authenticate(user=None)

        url = reverse('habits-public')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_access_private_habits(self):
        """Тест запрета доступа анонимного пользователя к приватным привычкам"""
        self.client.force_authenticate(user=None)

        url = reverse('habits-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_update_own_habit(self):
        """Тест возможности владельца обновлять свою привычку"""
        self.client.force_authenticate(user=self.owner)

        url = reverse('habits-detail', args=[self.habit.id])
        data = {'place': 'Новое место'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_update_habit(self):
        """Тест запрета обновления привычки другим пользователем"""
        self.client.force_authenticate(user=self.other_user)

        url = reverse('habits-detail', args=[self.habit.id])
        data = {'place': 'Новое место'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)