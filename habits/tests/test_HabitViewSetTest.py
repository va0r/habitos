import os
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status

from habits.models import Habit, User
from habits.serializers import HabitSerializer
from habits.views import HabitViewSet
from users.managers import CustomUserManager


class HabitViewSetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="testuser@example.com", password="password", telegram_id ='6309910328')
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')

    @patch('habits.views.send_telegram_message')
    def test_perform_create_success(self, mock_send_telegram_message):
        # Задаем данные для теста
        habit_data = {'action': 'New Habit', 'user': self.user.id}
        serializer = HabitSerializer(data=habit_data)

        # Создаем валидный объект Habit
        serializer.is_valid(raise_exception=True)

        # Мокаем send_telegram_message, чтобы избежать реальной отправки сообщения
        mock_send_telegram_message.return_value = {'ok': True, 'result': {}}

        # Создаем вьюсет
        viewset = HabitViewSet()

        # Вызываем perform_create
        response = viewset.perform_create(serializer)

        # Проверяем, что send_telegram_message был вызван с правильными параметрами
        mock_send_telegram_message.assert_called_once_with(self.token, self.user.telegram_id,
                                                           f"Привет! Вы успешно создали новую привычку: {habit_data['action']}")

        # Проверяем, что возвращается ожидаемый ответ
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что объект Habit был успешно создан
        self.assertTrue(Habit.objects.filter(action='New Habit', user=self.user).exists())

    @patch('habits.views.send_telegram_message')
    def test_perform_create_failure(self, mock_send_telegram_message):
        # Задаем данные для теста
        habit_data = {'action': 'New Habit', 'user': self.user.id}
        serializer = HabitSerializer(data=habit_data)

        # Создаем валидный объект Habit
        serializer.is_valid(raise_exception=True)

        # Мокаем send_telegram_message, чтобы вызвать исключение
        mock_send_telegram_message.side_effect = Exception("Test exception")

        # Создаем вьюсет
        viewset = HabitViewSet()

        # Вызываем perform_create
        response = viewset.perform_create(serializer)

        # Проверяем, что возвращается ожидаемый ответ при ошибке
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Проверяем, что объект Habit не был создан
        self.assertFalse(Habit.objects.filter(action='New Habit', user=self.user).exists())
