from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        User = get_user_model()  # Переместим импорт сюда
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = User(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
