from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Habit(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место'
    )
    time = models.TimeField(
        verbose_name='Время'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        related_name='related_habits'
    )
    periodicity = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        default='daily',
        verbose_name='Периодичность'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение'
    )
    execution_time = models.PositiveIntegerField(
        verbose_name='Время на выполнение (в секундах)',
        help_text='Время в секундах'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user}: {self.action} в {self.time}"

    def clean(self):
        if self.execution_time > 120:
            raise ValidationError({
                'execution_time': 'Время выполнения не должно превышать 120 секунд.'
            })

        if self.related_habit and self.reward:
            raise ValidationError(
                'Нельзя одновременно указывать связанную привычку и вознаграждение.'
            )

        if self.is_pleasant and (self.related_habit or self.reward):
            raise ValidationError(
                'У приятной привычки не может быть вознаграждения или связанной привычки.'
            )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError({
                'related_habit': 'В связанные привычки могут попадать только приятные привычки.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)