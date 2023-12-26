import os
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Habit
from .send_telegram_message import send_telegram_message


@shared_task
def send_habit_notification():
    now_datetime = timezone.now() + timedelta(hours=3)
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    habits_with_users = Habit.objects.filter(user__telegram_id__isnull=False).prefetch_related('user')

    for habit in habits_with_users:
        habit_last_datetime = habit.last_action_datetime + timedelta(hours=3)
        frequency = habit.frequency
        time = habit.time
        habit_next_datetime = habit_last_datetime + timedelta(days=frequency, hours=time.hour, minutes=time.minute - 5)
        if habit_next_datetime <= now_datetime:
            message = f'Через 5 минут необходимо выполнять вашу привычку! ' \
                      f'Вам необходимо выполнить: {habit.action} ' \
                      f'После этого вы сможете вознаградить себя: {habit.reward if habit.reward else habit.related_habit}'
            habit.last_action_datetime = now_datetime - timedelta(hours=3)
            habit.save()
            send_telegram_message(token=token, telegram_id=habit.user.telegram_id, message=message)
