from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_pleasant', 'periodicity']

    def get_queryset(self):
        if self.action == 'public':
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == 'public':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwner()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def public(self, request):
        habits = self.get_queryset()
        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)