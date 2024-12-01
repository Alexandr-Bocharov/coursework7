from django.contrib.auth.models import AbstractUser
from django.db import models
from utils import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name="почта", unique=True)

    tg_chat_id = models.CharField(
        verbose_name="телеграм chat-id", **NULLABLE, max_length=100
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
