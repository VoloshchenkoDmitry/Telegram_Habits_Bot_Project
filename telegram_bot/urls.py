from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TelegramUserViewSet

router = DefaultRouter()
router.register('telegram', TelegramUserViewSet, basename='telegram')

urlpatterns = [
    path('', include(router.urls)),
]