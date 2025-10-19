from rest_framework import serializers
from .models import Habit
from .validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'related_habit', 'periodicity', 'reward', 'execution_time',
            'is_public', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        validator = HabitValidator(data, instance=self.instance)
        validator.validate()
        return data