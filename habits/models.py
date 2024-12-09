from django.db import models

from users.models import User
from utils import NULLABLE
from datetime import datetime


class Habit(models.Model):
    class Periodicity(models.TextChoices):
        MINUTELY = "minutely", "ежеминутно"
        HOURLY = "hourly", "ежечасно"
        DAILY = "daily", "ежедневно"
        WEEKLY = "weekly", "еженедельно"

    user = models.ForeignKey(
        User, verbose_name="пользователь", on_delete=models.CASCADE, **NULLABLE
    )
    place = models.CharField(max_length=150, verbose_name="место", **NULLABLE)
    tm = models.TimeField(verbose_name="время", **NULLABLE)
    action = models.CharField(max_length=200, verbose_name="действие")
    is_nice_habit = models.BooleanField(
        verbose_name="признак приятной привычки", default=False
    )
    related_habit = models.ForeignKey(
        "self", verbose_name="связанная привычка", **NULLABLE, on_delete=models.SET_NULL
    )
    periodicity = models.CharField(
        max_length=20,
        verbose_name="периодичность",
        choices=Periodicity.choices,
        default=Periodicity.DAILY,
    )
    reward = models.CharField(max_length=100, verbose_name="Вознаграждение", **NULLABLE)
    time_to_complete = models.TimeField(verbose_name="время на выполнение", **NULLABLE)
    is_published = models.BooleanField(
        verbose_name="признак публичности", default=False
    )

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"
