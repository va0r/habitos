import random

from django.core.management.base import BaseCommand
from django.db import connections
from faker import Faker

from users.managers import CustomUserManager
from users.models import User, UserRoles


class Command(BaseCommand):
    help = 'Generate 10-15 users with role "member"'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Deleting existing users...'))
        User.objects.exclude(email__in=['admin@admin.admin', 'mod@mod.mod']).delete()
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('users_user', 'id'), 3, false)")

        self.stdout.write(self.style.SUCCESS('Generating users...'))

        fake = Faker('ru_Ru')
        manager = CustomUserManager()

        for _ in range(random.randint(10, 15)):
            email = fake.email()
            password = fake.password()
            phone = fake.phone_number()
            city = fake.city()
            avatar = fake.image_url()
            telegram_id = 'sotibah'

            user = manager.create_user(
                email=email,
                password=password,
                phone=phone,
                city=city,
                avatar=avatar,
                telegram_id=telegram_id,
                role=UserRoles.MEMBER
            )

            self.stdout.write(self.style.SUCCESS(f'User created: {user}'))

        self.stdout.write(self.style.SUCCESS('User generation completed successfully!'))
