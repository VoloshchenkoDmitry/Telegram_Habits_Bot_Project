import os
import django
from django.conf import settings

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from telegram_bot.bot import HabitBot

def test_bot_connection():
    try:
        bot = HabitBot()
        print("✅ Bot initialized successfully!")
        print(f"🤖 Bot name: {bot.name}")
        print(f"📱 Bot username: @{bot.username}")
        print("✅ Telegram token is valid!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_bot_connection()
