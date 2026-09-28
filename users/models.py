from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название отдела"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"

    def __str__(self):
        return self.name

class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGER = "MANAGER", "Менеджер"
        EMPLOYEE = "EMPLOYEE", "Сотрудник"

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Отдел",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
        verbose_name="Роль",
    )
    patronymic = models.CharField(
        max_length=150, blank=True, verbose_name="Отчество"
    )

    def is_manager(self):
        return self.role == self.Role.MANAGER or self.is_superuser

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
