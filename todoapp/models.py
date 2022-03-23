from django.db import models
from django.db.models import CASCADE
from usersapp.models import User


class Project(models.Model):
    title = models.CharField(max_length=255)
    repository_link = models.URLField()
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.title}"


class ToDo(models.Model):

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

    def __str__(self):
        status = 'active' if self.status else 'closed'
        return f"{self.text}, updated: {self.updated_at}, status: {status}"
