from datetime import time

from django.contrib.auth import get_user_model
from django.test import TestCase

from habits.models import Habit

User = get_user_model()


class HabitModelpyTestCase(TestCase):
    def test_user_field(self):
        user = User.objects.create(email="testuser@example.com", password="password")
        habit = Habit.objects.create(
            user=user,
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        self.assertEqual(habit.user, user)

    def test_place_field(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            place="Home",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        self.assertEqual(habit.place, "Home")

    def test_time_field(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            time=time(8, 0, 0),
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        self.assertEqual(habit.time, time(8, 0, 0))

    def test_action_field(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        self.assertEqual(habit.action, "Morning exercise")

    def test_is_pleasant_habit_field(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            is_pleasant_habit=True,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        self.assertTrue(habit.is_pleasant_habit)

    def test_related_habit_field(self):
        habit1 = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        habit2 = Habit.objects.create(
            user=User.objects.create(email="testuser1@example.com", password="password"),
            action="Evening exercise",
            is_pleasant_habit=True,
            frequency=7,
            estimated_time=2,
            is_public=False,
            related_habit=habit1,
        )
        self.assertEqual(habit2.related_habit, habit1)

    def test_frequency_field(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        self.assertEqual(habit.frequency, 7)

    def test_estimated_time_field(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        self.assertEqual(habit.estimated_time, 2)

    def test_is_public_field(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=True,
        )
        self.assertTrue(habit.is_public)

    def test_reward_field(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
            reward="Brew a cup of coffee",
        )
        self.assertEqual(habit.reward, "Brew a cup of coffee")

    def test_str_representation(self):
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
        self.assertEqual(str(habit), f"{user} - {habit.action}")

    def test_habit_creation(self):
        user = User.objects.create(email="testuser@example.com", password="password")
        Habit.objects.create(
            user=user,
            place="Home",
            time=time(8, 0, 0),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        self.assertEqual(Habit.objects.count(), 1)

    def test_habit_str_representation_with_pleasant_habit(self):
        user = User.objects.create(email="testuser@example.com", password="password")
        habit = Habit.objects.create(
            user=user,
            place="Home",
            time=time(8, 0, 0),
            action="Morning exercise",
            is_pleasant_habit=True,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        expected_str = f"{user} - {habit.action} (pleasant habit)"
        self.assertEqual(str(habit), expected_str)

    def test_habit_str_representation_with_public_habit(self):
        user = User.objects.create(email="testuser@example.com", password="password")
        habit = Habit.objects.create(
            user=user,
            place="Home",
            time=time(8, 0, 0),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=True,
        )
        expected_str = f"{user} - {habit.action} (public)"
        self.assertEqual(str(habit), expected_str)

    def test_related_habit_set_to_null(self):
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
        self.assertIsNone(habit.related_habit)

    def test_habit_with_related_habit(self):
        user = User.objects.create(email="testuser@example.com", password="password")
        habit1 = Habit.objects.create(
            user=user,
            place="Home",
            time=time(8, 0, 0),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        habit2 = Habit.objects.create(
            user=user,
            place="Home",
            time=time(8, 0, 0),
            action="Evening exercise",
            is_pleasant_habit=True,
            frequency=7,
            estimated_time=2,
            is_public=False,
            related_habit=habit1,
        )
        self.assertEqual(habit2.related_habit, habit1)

    def test_habit_str_representation(self):
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
        expected_str = f"{user} - {habit.action}"
        self.assertEqual(str(habit), expected_str)

    def test_calculate_next_notification_time_method(self):
        habit = Habit.objects.create(
            user=User.objects.create(email="testuser@example.com", password="password"),
            action="Morning exercise",
            is_pleasant_habit=False,
            frequency=7,
            estimated_time=2,
            is_public=False,
        )
        self.assertEqual(habit.calculate_next_notification_time(), None)
