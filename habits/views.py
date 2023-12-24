import os

from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly, CanReadPublicHabits
from habits.send_telegram_message import send_telegram_message
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]  # Применение кастомных прав доступа

    def perform_create(self, serializer):
        # Сначала создаем привычку
        habit = serializer.save()

        # Получите токен бота и чат-айди из настроек вашего приложения Telegram
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = habit.user.telegram_id

        # Отправляем приветственное сообщение
        message = f"Привет! Вы успешно создали новую привычку: {habit.action}"

        try:
            send_telegram_message(token, chat_id, message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Обработка ошибок отправки сообщения
            print(f"Ошибка отправки сообщения: {e}")
            habit.delete()
            return Response({"error": "Не удалось отправить приветственное сообщение"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Habit.objects.filter(is_public=True)  # Фильтр публичных привычек
    serializer_class = HabitSerializer
    permission_classes = [CanReadPublicHabits]  # Применение кастомных прав доступа
