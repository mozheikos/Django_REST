# Generated by Django 3.2 on 2022-03-22 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TODO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'Active'), (0, 'Closed')], default=1)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todoapp.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
