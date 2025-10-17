from django.urls import path
from .views import TelegramUserLinkView

urlpatterns = [
    path('telegram/link/', TelegramUserLinkView.as_view(), name='telegram-link'),
]
