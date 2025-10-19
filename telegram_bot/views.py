from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TelegramUser
from .serializers import TelegramUserSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TelegramUser.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def disconnect(self, request):
        """Отключает Telegram от аккаунта"""
        try:
            telegram_user = TelegramUser.objects.get(user=request.user)
            telegram_user.delete()
            return Response(
                {'message': 'Telegram успешно отключен от вашего аккаунта.'},
                status=status.HTTP_200_OK
            )
        except TelegramUser.DoesNotExist:
            return Response(
                {'error': 'Telegram не подключен к вашему аккаунту.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def toggle_notifications(self, request):
        """Включает/выключает уведомления"""
        try:
            telegram_user = TelegramUser.objects.get(user=request.user)
            telegram_user.is_active = not telegram_user.is_active
            telegram_user.save()

            status_text = 'включены' if telegram_user.is_active else 'выключены'
            return Response(
                {'message': f'Уведомления {status_text}.'},
                status=status.HTTP_200_OK
            )
        except TelegramUser.DoesNotExist:
            return Response(
                {'error': 'Telegram не подключен к вашему аккаунту.'},
                status=status.HTTP_400_BAD_REQUEST
            )