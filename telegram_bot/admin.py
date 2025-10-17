from django.contrib import admin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_chat_id', 'username', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'username')
    readonly_fields = ('created_at',)