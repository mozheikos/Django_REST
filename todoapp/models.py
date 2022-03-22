from django.db import models
from django.db.models import CASCADE

from usersapp.models import User


class Project(models.Model):
    title = models.CharField(max_length=255)
    repository_link = models.URLField()
    users = models.ManyToManyField(User)


class TODO(models.Model):

    STATUS_CHOICES = (
        (1, "Active"),
        (0, "Closed")
    )

    project = models.ForeignKey(Project, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
