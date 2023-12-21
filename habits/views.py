from rest_framework import viewsets

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly, CanReadPublicHabits
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Применение кастомных прав доступа


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Habit.objects.filter(is_public=True)  # Фильтр публичных привычек
    serializer_class = HabitSerializer
    permission_classes = [CanReadPublicHabits]  # Применение кастомных прав доступа
