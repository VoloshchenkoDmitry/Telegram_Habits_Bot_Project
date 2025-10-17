from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'place', 'time', 'is_pleasant', 'is_public')
    list_filter = ('is_pleasant', 'is_public', 'periodicity')
    search_fields = ('action', 'place', 'user__email')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'place', 'time', 'action')
        }),
        ('Тип и связь', {
            'fields': ('is_pleasant', 'related_habit', 'periodicity')
        }),
        ('Вознаграждение и время', {
            'fields': ('reward', 'execution_time')
        }),
        ('Видимость', {
            'fields': ('is_public',)
        }),
        ('Даты', {
            'fields': ('created_at',)
        }),
    )