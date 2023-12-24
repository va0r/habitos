from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from config.constants import NULLABLE

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits', verbose_name=_('User'), **NULLABLE)
    place = models.CharField(max_length=255, verbose_name=_('Place'), **NULLABLE)
    time = models.TimeField(verbose_name=_('Time'), **NULLABLE)
    action = models.CharField(max_length=255, verbose_name=_('Action'))
    is_pleasant_habit = models.BooleanField(default=False, verbose_name=_('Is Pleasant Habit'), **NULLABLE)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE, verbose_name=_('Related Habit'))
    frequency = models.PositiveIntegerField(default=10, verbose_name=_('Frequency (days)'), **NULLABLE)
    reward = models.CharField(max_length=255, verbose_name=_('Reward'), **NULLABLE)
    estimated_time = models.PositiveIntegerField(default=10, verbose_name=_('Estimated Time (minutes)'), **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name=_('Is Public'), **NULLABLE)

    def calculate_next_notification_time(self):
        if self.time is not None:
            now = timezone.now()
            today = now.date()
            habit_time = datetime.combine(today, self.time)
            habit_time = timezone.make_aware(habit_time, timezone.get_current_timezone())

            while habit_time <= now:
                habit_time += timedelta(days=self.frequency)
            return habit_time
        return None

    def save(self, *args, **kwargs):
        if self.time is not None:
            self.next_notification_time = self.calculate_next_notification_time()
        super().save(*args, **kwargs)

    def __str__(self):
        labels = []
        if self.is_public:
            labels.append("public")
        if self.is_pleasant_habit:
            labels.append("pleasant habit")
        label_str = " (" + ", ".join(labels) + ")" if labels else ""
        return f'{self.user} - {self.action}{label_str}'

    class Meta:
        verbose_name = _('Habit')
        verbose_name_plural = _('Habits')
