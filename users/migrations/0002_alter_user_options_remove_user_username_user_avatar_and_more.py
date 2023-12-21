# Generated by Django 5.0 on 2023-12-21 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user/', verbose_name='Avatar'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Phone'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('member', 'Member'), ('moderator', 'Moderator')], default='member', max_length=9),
        ),
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Telegram ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
    ]
