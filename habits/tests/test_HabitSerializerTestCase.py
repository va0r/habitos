from datetime import time

from django.contrib.auth import get_user_model
from django.test import TestCase

from habits.models import Habit
from habits.serializers import HabitSerializer

User = get_user_model()


class HabitSerializerTestCase(TestCase):
    def test_valid_habit(self):
        data = {
            "action": "Morning exercise",
            "is_pleasant_habit": False,
            "frequency": 7,
            "estimated_time": 30,
            "is_public": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_habit_serializer_validation(self):
        data = {
            "user": 1,
            "place": "Home",
            "time": time(8, 0, 0),
            "action": "Morning exercise",
            "is_pleasant_habit": True,
            "related_habit": None,
            "frequency": 7,
            "reward": None,
            "estimated_time": 2,
            "is_public": False,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_habit_serializer_invalid_related_habit(self):
        data = {
            "user": 1,
            "action": "Morning exercise",
            "related_habit": 2,  # Неверный идентификатор связанной привычки
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("related_habit", serializer.errors)

    def test_estimated_time(self):
        data = {
            "action": "Morning exercise",
            "estimated_time": 200
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_frequency(self):
        data = {
            "action": "Morning exercise",
            "frequency": 1,
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_habit_serializer_invalid_related_habit_reward(self):
        related_data = {
            "action": "Evening exercise",
            "is_pleasant_habit": True,
        }
        related_habit = Habit.objects.create(**related_data)

        data = {
            "action": "Morning exercise",
            "related_habit": related_habit.id,
            "reward": "Ops"
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_habit_serializer_invalid_related_habit_is_pleasant(self):
        related_data = {
            "action": "Evening exercise",
            "is_pleasant_habit": False,
        }
        related_habit = Habit.objects.create(**related_data)

        data = {
            "action": "Morning exercise",
            "related_habit": related_habit.id,
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_habit_serializer_invalid_pleasant_habit(self):
        data = {
            "action": "Morning exercise",
            "is_pleasant_habit": True,
            "reward": "Ops"
        }

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
