import os
from datetime import datetime, timedelta

from celery import shared_task
from django.utils import timezone

from .models import Habit
from .send_telegram_message import send_telegram_message


@shared_task
def send_habit_notification():
    now_time = timezone.now() + timedelta(hours=2)  # расчет времени для региона
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    habits_with_users = Habit.objects.filter(user__telegram_id__isnull=False).prefetch_related('user')

    for habit in habits_with_users:
        habit_time = datetime.combine(now_time.date(), habit.time)
        habit_time_aware = timezone.make_aware(habit_time, now_time.tzinfo)

        if habit_time_aware <= now_time - timedelta(minutes=5):
            message = f'Через 5 минут необходимо выполнять вашу привычку! ' \
                      f'Вам необходимо выполнить: {habit.action} ' \
                      f'После этого вы сможете вознаградить себя: {habit.reward if habit.reward else habit.related_habit}'
            send_telegram_message(token=token, telegram_id=habit.user.telegram_id, message=message)
