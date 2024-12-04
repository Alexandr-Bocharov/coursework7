from rest_framework import serializers
from datetime import time


class ValidateRelatedHabitAndReward:

    def __call__(self, data, instance=None):

        if instance:
            is_nice_habit = instance.is_nice_habit
            if not is_nice_habit:
                current_reward = instance.reward
                current_related_habit = instance.related_habit

                if current_reward and current_related_habit:
                    raise serializers.ValidationError(
                        "У полезной привычки может быть только одно из полей: награда или связанная привычка."
                    )
        else:
            is_nice_habit = data.get("is_nice_habit")
            if not is_nice_habit:
                new_reward = data.get("reward")
                new_related_habit = data.get("related_habit")

                if new_reward and new_related_habit:
                    message = "у полезной привычки может быть что-то одно: награда или связанная привычка"
                    raise serializers.ValidationError(message)


class ValidateTimeToComplete:
    def __init__(self, field):
        self.field = field

    def __call__(self, value, instance=None):
        time_to_complete = value.get("time_to_complete")
        if time_to_complete:
            if time_to_complete > time(minute=2):
                raise serializers.ValidationError(
                    "Время выполнения привычки не может быть больше 120 секунд"
                )


class ValidateRelatedHabit:
    def __init__(self, field):
        self.field = field

    def __call__(self, value, instance=None):
        related_habit = value.get("related_habit")
        if related_habit:
            if not related_habit.is_nice_habit:
                raise serializers.ValidationError(
                    "В связанные привычки могут попадать только привычки с признаком приятной привычки."
                )


class ValidateNiceHabit:
    def __call__(self, data, instance=None):

        message = (
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )

        if instance:
            is_nice_habit = instance.is_nice_habit
            if is_nice_habit:
                cur_reward = data.get('reward')
                cur_related_habit = data.get("related_habit")
                if cur_reward or cur_related_habit:
                    raise serializers.ValidationError(message)
        else:
            is_nice_habit = data.get("is_nice_habit")
            if is_nice_habit:
                new_reward = data.get("reward")
                new_related_habit = data.get("related_habit")
                if new_reward or new_related_habit:
                    raise serializers.ValidationError(message)
