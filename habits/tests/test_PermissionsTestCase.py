from datetime import time

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly, CanReadPublicHabits

User = get_user_model()


class PermissionsTestCase(TestCase):
    def test_owner_has_edit_permissions(self):
        user = User.objects.create(email="testuser@example.com", password="password")
        habit = Habit.objects.create(
            user=user,
            place="Home",
            time=time(8, 0, 0),
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
            time=time(8, 0, 0),
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
            time=time(8, 0, 0),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        request_factory = RequestFactory()
        request = request_factory.get("/")
        # Создаем объект
        permission_IsOwnerOrReadOnly = IsOwnerOrReadOnly()
        permission_CanReadPublicHabits = CanReadPublicHabits()
        self.client.logout()  # Делаем пользователя анонимным
        self.assertTrue(permission_IsOwnerOrReadOnly.has_object_permission(request, None, habit))
        self.assertTrue(permission_CanReadPublicHabits.has_permission(request, None))

    def test_has_object_permission(self):
        user = User.objects.create(email="testuser@example.com", password="password")
        habit = Habit.objects.create(
            user=user,
            place="Home",
            time=time(8, 0, 0),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )

        # Создаем запрос
        request_factory = RequestFactory()
        request = request_factory.post("/")
        request.user = user  # Устанавливаем пользователя вручную

        # Создаем объект
        permission_IsOwnerOrReadOnly = IsOwnerOrReadOnly()
        permission_CanReadPublicHabits = CanReadPublicHabits()

        # Проверяем, что метод возвращает ожидаемое значение
        self.assertTrue(permission_IsOwnerOrReadOnly.has_object_permission(request, None, habit))
        self.assertFalse(permission_CanReadPublicHabits.has_permission(request, None))
