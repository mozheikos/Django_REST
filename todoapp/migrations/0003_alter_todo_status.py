# Generated by Django 3.2 on 2022-03-24 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_todo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('closed', 'Closed')], default='active', max_length=6),
        ),
    ]
