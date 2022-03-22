from django.db import models
from usersapp.models import User


class Project(models.Model):
    title = models.CharField(max_length=255)
    repository_link = models.URLField()
    users = models.ManyToManyField(User)
