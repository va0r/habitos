# Generated by Django 4.2.8 on 2023-12-26 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='estimated_time',
            field=models.PositiveIntegerField(blank=True, default=10, null=True, verbose_name='Estimated Time (minutes)'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='frequency',
            field=models.PositiveIntegerField(blank=True, default=10, null=True, verbose_name='Frequency (days)'),
        ),
    ]
