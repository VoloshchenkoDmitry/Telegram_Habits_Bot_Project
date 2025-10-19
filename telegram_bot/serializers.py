from rest_framework import serializers
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = [
            'id', 'telegram_chat_id', 'username', 'first_name',
            'last_name', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'telegram_chat_id', 'username', 'first_name',
            'last_name', 'created_at', 'updated_at'
        ]