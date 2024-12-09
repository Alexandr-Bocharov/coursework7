from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import CustomHabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer

from habits.tasks import send_tg_message, send_tg_message_after_create


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        send_tg_message_after_create.delay(habit.pk)
        habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UsefulHabitListAPIView(generics.ListAPIView):
    """Список полезных привычек, которые создал текущий пользователь"""

    serializer_class = HabitSerializer
    pagination_class = CustomHabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user, is_nice_habit=False)


class NiceHabitListAPIView(generics.ListAPIView):
    """Список приятных привычек, которые создал текущий пользователь"""

    serializer_class = HabitSerializer
    pagination_class = CustomHabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user, is_nice_habit=True)


class PublicUsefulHabitListAPIView(generics.ListAPIView):
    """Список публичных полезных привычек"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_published=True, is_nice_habit=False)


class PublicNiceHabitListAPIView(generics.ListAPIView):
    """Список публичных приятных привычек"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_published=True, is_nice_habit=True)
