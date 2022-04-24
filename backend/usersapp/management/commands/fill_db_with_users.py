from django.core.management.base import BaseCommand
from usersapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        number_of_users = 30
        user = User.objects.filter(username='admin').first()
        if not user:
            superuser = User.objects.create_superuser(username='admin', email='admin@mail.ru', password='admin',
                                                          first_name='admin', last_name='God')
            superuser.save()

        start = User.objects.order_by("id").last().id + 1

        for i in range(start, number_of_users + start + 1):
            user = User.objects.create_user(username=f'user_{i}', email=f'user_{i}@mail.ru', password=f'user_{i}',
                                            first_name=f'some_first_name_{i}', last_name=f'some_last_name_{i}')
            user.save()
