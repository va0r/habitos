from django.core.management.base import BaseCommand
from django.db import connections

from habits.models import Habit
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Habit.objects.all().delete()
        User.objects.exclude(email__in=['admin@admin.admin', 'mod@mod.mod']).delete()

