from django.core.management.base import BaseCommand
from usersapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        number_of_users = int(input("How many users (exclude superuser) you want to create? "))
        superuser = User.objects.create_superuser(username='admin', email='admin@mail.ru', password='admin',
                                                  first_name='admin', last_name='God')
        superuser.save()
        for i in range(1, number_of_users + 1):
            user = User.objects.create_user(username=f'user_{i}', email=f'user_{i}@mail.ru', password=f'user_{i}',
                                            first_name=f'some_first_name_{i}', last_name=f'some_last_name_{i}')
            user.save()
