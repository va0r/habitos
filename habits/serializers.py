from types import NoneType

from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        related_habit = data.get('related_habit')
        reward = data.get('reward')
        estimated_time = data.get('estimated_time', 10)
        is_pleasant_habit = data.get('is_pleasant_habit', False)
        frequency = data.get('frequency', 1)

        if related_habit and reward:
            raise serializers.ValidationError(
                'Привычка не может иметь одновременно связанную привычку и вознаграждение.'
            )

        if type(estimated_time) is not NoneType and int(estimated_time) > 120:
            raise serializers.ValidationError(
                'Оценочное время выполнения не должно превышать 120 мин.'
            )

        if related_habit and not related_habit.is_pleasant_habit:
            raise serializers.ValidationError(
                'Связанная привычка должна быть приятной привычкой.'
            )

        if is_pleasant_habit:
            if reward or related_habit:
                raise serializers.ValidationError(
                    'Приятная привычка не может иметь вознаграждение или связанную привычку.'
                )

        if type(frequency) is not NoneType and int(frequency) > 7:
            raise serializers.ValidationError(
                'Частота выполнения привычки не должна быть больше 7 дней.'
            )

        return data
