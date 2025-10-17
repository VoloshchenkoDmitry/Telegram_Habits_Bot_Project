from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TelegramUser
from .serializers import TelegramUserSerializer


class TelegramUserLinkView(generics.CreateAPIView):
    serializer_class = TelegramUserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        telegram_user, created = TelegramUser.objects.update_or_create(
            user=request.user,
            defaults=serializer.validated_data
        )

        return Response(
            {'message': 'Telegram успешно привязан' if created else 'Данные обновлены'},
            status=status.HTTP_201_CREATED
        )