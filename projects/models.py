from django.db import models
from django.conf import settings

from constants.projects import ProjectStatus

class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = ProjectStatus.OPEN, "Open"
        CLOSED = ProjectStatus.CLOSED, "Closed"

    name = models.CharField(
        max_length=200,
        verbose_name="Название проекта",
        help_text="Введите название проекта (до 200 символов)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание проекта",
        help_text="Введите описание проекта (необязательно)"
    )
    github_url = models.URLField(
        blank=True,
        verbose_name="URL репозитория на GitHub",
        help_text="Введите URL репозитория на GitHub (необязательно)"
    )
    status = models.CharField(
        max_length=max(map(len, Status.values)),
        choices=Status,
        default=Status.OPEN,
        verbose_name="Статус проекта",
        help_text="Выберите статус проекта"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания проекта"
    )
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='owned_projects',
        on_delete=models.CASCADE
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participated_projects',
        blank=True
    )