import random
from datetime import time

from django.core.management.base import BaseCommand
from django.db import connections
from faker import Faker

from habits.models import Habit
from users.models import User


class Command(BaseCommand):
    help = 'Generate 20-30 different useful habits'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating habits...'))

        # Delete all data and reset sequence for each table to 1
        Habit.objects.all().delete()
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('habits_habit', 'id'), 1, false)")

        fake = Faker('')
        users = list(User.objects.exclude(email__in=['admin@admin.admin', 'mod@mod.mod']).all())

        for _ in range(random.randint(20, 30)):
            user = random.choice(users)
            is_pleasant_habit = random.choice([True, False])
            is_public = random.choice([True, False])

            habit = Habit.objects.create(
                user=user,
                place=fake.word(),
                time=time(hour=random.randint(9, 21), minute=random.randint(0, 59)),
                action=fake.sentence(),
                is_pleasant_habit=is_pleasant_habit,
                related_habit=None,  # You can customize this as needed
                frequency=random.randint(1, 7),
                reward=fake.word(),
                estimated_time=random.randint(1, 60),
                is_public=is_public
            )

            self.stdout.write(self.style.SUCCESS(f'Habit created: {habit}'))

        self.stdout.write(self.style.SUCCESS('Habit generation completed successfully!'))
