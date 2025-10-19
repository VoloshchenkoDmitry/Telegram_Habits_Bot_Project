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
        ('Тип привычки', {
            'fields': ('is_pleasant', 'related_habit', 'reward')
        }),
        ('Настройки', {
            'fields': ('periodicity', 'execution_time', 'is_public')
        }),
        ('Даты', {
            'fields': ('created_at',)
        }),
    )