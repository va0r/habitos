from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from constants import NULLABLE
from users.managers import CustomUserManager


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('Member')
    MODERATOR = 'moderator', _('Moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    telegram_id = models.CharField(max_length=255, verbose_name=_('Telegram ID'), **NULLABLE)

    phone = models.CharField(max_length=35, verbose_name=_('Phone'), **NULLABLE)
    city = models.CharField(max_length=150, verbose_name=_('City'), **NULLABLE)
    avatar = models.ImageField(upload_to='user/', verbose_name=_('Avatar'), **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
