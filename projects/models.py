from django.db import models
from django.conf import settings

from constants.projects import ProjectStatus

class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = ProjectStatus.OPEN, "Open"
        CLOSED = ProjectStatus.CLOSED, "Closed"

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_projects', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(max_length=max(map(len, Status.values)), choices=Status, default=Status.OPEN)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participated_projects', blank=True)