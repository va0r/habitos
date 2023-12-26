import os
import unittest
from unittest.mock import patch
from django.test import TestCase

from habits.send_telegram_message import send_telegram_message


class TelegramMessageTest(TestCase):

    @patch('requests.post')  # Мокаем requests.post
    def test_send_telegram_message(self, mock_post):
        # Устанавливаем ожидаемый ответ от API Telegram
        mock_post.return_value.json.return_value = {'ok': True, 'result': {}}

        # Задаем данные для теста
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_id = '6309910328'
        message = 'Test message'

        # Вызываем функцию
        result = send_telegram_message(token, telegram_id, message)

        # Проверяем, что requests.post был вызван с правильными параметрами
        mock_post.assert_called_once_with(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={'chat_id': telegram_id, 'text': message}
        )

        # Проверяем, что функция возвращает ожидаемый результат
        self.assertEqual(result, {'ok': True, 'result': {}})
