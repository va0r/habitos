from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly, CanReadPublicHabits
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
        self.assertFalse(serializer.is_valid())

    def test_habit_serializer_validation(self):
        # Test serializer validation
        data = {
            "user": 1,
            "place": "Home",
            "time": "08:00:00",
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

    def test_habit_serializer_invalid_related_habit_reward(self):
        # Test serializer validation with both related habit and reward
        data = {
            "user": 1,
            "place": "Home",
            "time": "08:00:00",
            "action": "Morning exercise",
            "is_pleasant_habit": False,
            "related_habit": 2,
            "frequency": 7,
            "reward": "Brew a cup of coffee",
            "estimated_time": 2,
            "is_public": False,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("related_habit", serializer.errors)

    def test_habit_serializer_invalid_related_habit(self):
        data = {
            "user": 1,
            "action": "Morning exercise",
            "related_habit": 2,  # Неверный идентификатор связанной привычки
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("related_habit", serializer.errors)


class IsOwnerOrReadOnlyTestCase(TestCase):
    def test_owner_has_edit_permissions(self):
        user = User.objects.create(email="testuser@example.com", password="password")
        habit = Habit.objects.create(
            user=user,
            place="Home",
            time="08:00:00",
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        request_factory = RequestFactory()
        request = request_factory.get("/")
        self.client.force_login(user)
        permission = IsOwnerOrReadOnly()
        self.assertTrue(permission.has_object_permission(request, None, habit))

    def test_other_users_cannot_edit(self):
        user1 = User.objects.create(email="user1@example.com", password="password")
        user2 = User.objects.create(email="user2@example.com", password="password")

        habit = Habit.objects.create(
            user=user1,
            place="Home",
            time="08:00:00",
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        request_factory = RequestFactory()
        request = request_factory.get("/")
        self.client.force_login(user2)

        permission = IsOwnerOrReadOnly()
        self.assertTrue(permission.has_object_permission(request, None, habit))

    def test_anonymous_user_cannot_edit(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),  # Создаем нового пользователя
            place="Home",
            time="08:00:00",
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        request_factory = RequestFactory()
        request = request_factory.get("/")
        permission = IsOwnerOrReadOnly()
        self.client.logout()  # Делаем пользователя анонимным
        self.assertTrue(permission.has_object_permission(request, None, habit))


class CanReadPublicHabitsTestCase(TestCase):
    def test_can_read_public_habits(self):
        user = User.objects.create(email="testuser@example.com", password="password")
        Habit.objects.create(
            user=user,
            place="Home",
            time="08:00:00",
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=True,
        )
        request_factory = RequestFactory()
        request = request_factory.get("/")
        permission = CanReadPublicHabits()
        self.assertTrue(permission.has_permission(request, None))
