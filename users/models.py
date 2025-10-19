from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, default='')
    telegram_chat_id = models.BigIntegerField(null=True, blank=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Убираем username из REQUIRED_FIELDS

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Автоматически создаем username если он пустой
        if not self.username:
            self.username = f"user_{self.email.split('@')[0]}"
        super().save(*args, **kwargs)