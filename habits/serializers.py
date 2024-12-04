from rest_framework import serializers
from habits.validators import (
    ValidateRelatedHabitAndReward,
    ValidateTimeToComplete,
    ValidateRelatedHabit,
    ValidateNiceHabit,
)

from habits.models import Habit


class RelatedHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class HabitSerializer(serializers.ModelSerializer):
    related_habit = RelatedHabitSerializer()

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            ValidateRelatedHabitAndReward(),
            ValidateTimeToComplete(field="time_to_complete"),
            ValidateRelatedHabit(field="related_habit"),
            ValidateNiceHabit(),
        ]

    def run_validators(self, value):
        for validator in self.validators:
            if hasattr(validator, '__call__'):
                validator(value, instance=self.instance)


# class HabitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Habit
#         fields = "__all__"
#         validators = [
#             ValidateRelatedHabitAndReward(),
#             ValidateTimeToComplete(field="time_to_complete"),
#             ValidateRelatedHabit(field="related_habit"),
#             ValidateNiceHabit(),
#         ]
#
#     def run_validators(self, value):
#         for validator in self.validators:
#             if hasattr(validator, '__call__'):
#                 validator(value, instance=self.instance)
