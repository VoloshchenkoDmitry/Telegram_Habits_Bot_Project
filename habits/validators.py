from rest_framework import serializers


class HabitValidator:
    def __init__(self, data, instance=None):
        self.data = data
        self.instance = instance

    def validate(self):
        self._validate_execution_time()
        self._validate_related_habit_and_reward()
        self._validate_pleasant_habit()
        self._validate_related_habit_is_pleasant()
        self._validate_periodicity()

    def _validate_execution_time(self):
        execution_time = self.data.get('execution_time')
        if execution_time and execution_time > 120:
            raise serializers.ValidationError({
                'execution_time': 'Время выполнения не должно превышать 120 секунд.'
            })

    def _validate_related_habit_and_reward(self):
        related_habit = self.data.get('related_habit')
        reward = self.data.get('reward')

        if related_habit and reward:
            raise serializers.ValidationError(
                'Нельзя одновременно указывать связанную привычку и вознаграждение.'
            )

    def _validate_pleasant_habit(self):
        is_pleasant = self.data.get('is_pleasant', False)
        related_habit = self.data.get('related_habit')
        reward = self.data.get('reward')

        if is_pleasant and (related_habit or reward):
            raise serializers.ValidationError(
                'У приятной привычки не может быть вознаграждения или связанной привычки.'
            )

    def _validate_related_habit_is_pleasant(self):
        related_habit = self.data.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError({
                'related_habit': 'В связанные привычки могут попадать только приятные привычки.'
            })

    def _validate_periodicity(self):
        periodicity = self.data.get('periodicity', 'daily')
        if periodicity not in ['daily', 'weekly']:
            raise serializers.ValidationError({
                'periodicity': 'Периодичность должна быть "daily" или "weekly".'
            })