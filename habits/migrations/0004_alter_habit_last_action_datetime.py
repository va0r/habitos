# Generated by Django 4.2.8 on 2024-01-18 19:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_habit_last_action_datetime_alter_habit_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='last_action_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 1, 6, 0, tzinfo=datetime.timezone.utc), verbose_name='Last Action'),
        ),
    ]