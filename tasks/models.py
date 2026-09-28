from django.conf import settings
from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "Новая"
        IN_PROGRESS = "IN_PROGRESS", "В работе"
        COMPLETED = "COMPLETED", "Завершена"
        CANCELED = "CANCELED", "Отменена"

    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    due_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Срок выполнения"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Исполнитель",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tasks",
        verbose_name="Создал менеджер",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
